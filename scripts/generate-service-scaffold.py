#!/usr/bin/env python3
"""
Generate Spring Boot service scaffolds from OpenAPI specs.

Reads specs from architecture/specs/ and generates service projects in services/.
Follows established NovaTrek patterns from existing services (svc-guest-profiles,
svc-trip-catalog, svc-trail-management).

Usage:
    python3 scripts/generate-service-scaffold.py                    # Generate all missing services
    python3 scripts/generate-service-scaffold.py svc-check-in       # Generate specific service
    python3 scripts/generate-service-scaffold.py --list             # List services to generate
"""

import yaml
import os
import re
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# --- Configuration ---
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SPECS_DIR = WORKSPACE_ROOT / "architecture" / "specs"
SERVICES_DIR = WORKSPACE_ROOT / "services"
TEMPLATE_DIR = SERVICES_DIR / "template"

EXISTING_SERVICES = {"svc-guest-profiles", "svc-trip-catalog", "svc-trail-management"}

# OpenAPI type -> Java type
TYPE_MAP = {
    ("string", None): "String",
    ("string", "uuid"): "UUID",
    ("string", "date-time"): "OffsetDateTime",
    ("string", "date"): "LocalDate",
    ("string", "uri"): "String",
    ("string", "email"): "String",
    ("integer", None): "Integer",
    ("integer", "int32"): "Integer",
    ("integer", "int64"): "Long",
    ("number", None): "BigDecimal",
    ("number", "float"): "BigDecimal",
    ("number", "double"): "BigDecimal",
    ("boolean", None): "Boolean",
}

# Java type -> SQL column type
SQL_TYPE_MAP = {
    "String": "VARCHAR(255)",
    "UUID": "UUID",
    "OffsetDateTime": "TIMESTAMPTZ",
    "LocalDate": "DATE",
    "Integer": "INTEGER",
    "Long": "BIGINT",
    "BigDecimal": "NUMERIC(10,2)",
    "Boolean": "BOOLEAN",
}


def svc_to_pkg(svc: str) -> str:
    """svc-guest-profiles -> guestprofiles"""
    return svc.replace("svc-", "").replace("-", "")


def svc_to_class(svc: str) -> str:
    """svc-guest-profiles -> GuestProfiles"""
    return "".join(p.capitalize() for p in svc.replace("svc-", "").split("-"))


def svc_to_schema(svc: str) -> str:
    """svc-guest-profiles -> guest_profiles"""
    return svc.replace("svc-", "").replace("-", "_")


def snake_to_camel(name: str) -> str:
    """first_name -> firstName"""
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def snake_to_pascal(name: str) -> str:
    """first_name -> FirstName"""
    return "".join(p.capitalize() for p in name.split("_"))


def camel_to_snake(name: str) -> str:
    """firstName -> first_name, CheckIn -> check_in"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def resolve_ref(ref: str) -> str:
    """#/components/schemas/CheckIn -> CheckIn"""
    return ref.split("/")[-1]


def pluralize(name: str) -> str:
    """Simple pluralization for table names."""
    if name.endswith("s"):
        return name + "es"
    if name.endswith("y") and name[-2] not in "aeiou":
        return name[:-1] + "ies"
    return name + "s"


# Schemas to always skip (not entities)
SKIP_SCHEMAS = {
    "ErrorResponse", "Error", "Pagination",
}
SKIP_SUFFIXES = (
    "Request", "Create", "Update", "Page", "List",
    "Response", "Body",
)


class Field:
    """Represents a Java entity field."""

    def __init__(self, name: str, java_type: str, is_enum: bool = False,
                 enum_values: list = None, required: bool = False,
                 description: str = "", is_id: bool = False):
        self.spec_name = name  # original OpenAPI name (snake_case)
        self.java_name = snake_to_camel(name)  # camelCase
        self.col_name = name if "_" in name else camel_to_snake(name)
        self.java_type = java_type
        self.is_enum = is_enum
        self.enum_values = enum_values or []
        self.required = required
        self.description = description
        self.is_id = is_id


class EntityDef:
    """Represents a JPA entity to generate."""

    def __init__(self, name: str, fields: List[Field], table_name: str):
        self.name = name  # PascalCase class name
        self.fields = fields
        self.table_name = table_name


class EndpointDef:
    """Represents a REST endpoint."""

    def __init__(self, method: str, path: str, operation_id: str,
                 summary: str, response_code: str, response_schema: str,
                 request_schema: str = None, path_params: list = None,
                 query_params: list = None):
        self.method = method
        self.path = path
        self.operation_id = operation_id
        self.summary = summary
        self.response_code = response_code
        self.response_schema = response_schema
        self.request_schema = request_schema
        self.path_params = path_params or []
        self.query_params = query_params or []


class ResourceDef:
    """Represents a REST resource (controller)."""

    def __init__(self, base_path: str, endpoints: List[EndpointDef],
                 entity_name: str):
        self.base_path = base_path
        self.endpoints = endpoints
        self.entity_name = entity_name
        self.controller_name = snake_to_pascal(
            base_path.strip("/").split("/")[0].replace("-", "_")
        ) + "Controller"


class ServiceGenerator:
    """Generates a complete Spring Boot service from an OpenAPI spec."""

    def __init__(self, spec_path: Path):
        with open(spec_path) as f:
            self.spec = yaml.safe_load(f)

        self.svc_name = spec_path.stem
        self.pkg = svc_to_pkg(self.svc_name)
        self.class_prefix = svc_to_class(self.svc_name)
        self.db_schema = svc_to_schema(self.svc_name)
        self.svc_dir = SERVICES_DIR / self.svc_name

        self.schemas = self.spec.get("components", {}).get("schemas", {})
        self.paths = self.spec.get("paths", {})
        self.parameters = self.spec.get("components", {}).get("parameters", {})

        self.entities: List[EntityDef] = []
        self.resources: List[ResourceDef] = []
        self._analyze()

    def _analyze(self):
        """Analyze the spec to identify entities and resources."""
        entity_names = self._find_entity_names()
        for name in sorted(entity_names):
            fields = self._extract_fields(name)
            if fields:
                table = pluralize(camel_to_snake(name))
                self.entities.append(EntityDef(name, fields, table))

        self._build_resources()

    def _find_entity_names(self) -> Set[str]:
        """Identify schemas that should become JPA entities."""
        candidates = set()
        for name, schema in self.schemas.items():
            if name in SKIP_SCHEMAS:
                continue
            if any(name.endswith(s) for s in SKIP_SUFFIXES):
                continue
            if schema.get("type") != "object":
                continue

            props = schema.get("properties", {})
            # Must have an id-like field
            first_prop = list(props.keys())[0] if props else ""
            has_id = ("id" in props or
                      any(k == first_prop and props[k].get("format") == "uuid"
                          for k in props) or
                      any(k.endswith("_id") and props[k].get("format") == "uuid"
                          and k == first_prop for k in props))

            if has_id:
                candidates.add(name)

        return candidates

    def _extract_fields(self, schema_name: str) -> List[Field]:
        """Extract fields from a schema."""
        schema = self.schemas.get(schema_name, {})
        props = schema.get("properties", {})
        required_set = set(schema.get("required", []))
        fields = []

        # Determine the ID field name
        first_prop = list(props.keys())[0] if props else None
        id_field = None
        if "id" in props and props["id"].get("format") == "uuid":
            id_field = "id"
        elif first_prop and props[first_prop].get("format") == "uuid":
            id_field = first_prop

        for prop_name, prop in props.items():
            field = self._resolve_field(prop_name, prop, prop_name in required_set,
                                        is_id=(prop_name == id_field))
            if field:
                fields.append(field)

        return fields

    def _resolve_field(self, name: str, prop: dict, required: bool,
                       is_id: bool = False) -> Optional[Field]:
        """Convert an OpenAPI property to a Field."""
        # Handle $ref to enum
        if "$ref" in prop:
            ref_name = resolve_ref(prop["$ref"])
            ref_schema = self.schemas.get(ref_name, {})
            if ref_schema.get("type") == "string" and "enum" in ref_schema:
                return Field(name, ref_name, is_enum=True,
                             enum_values=ref_schema["enum"],
                             required=required,
                             description=prop.get("description", ""))
            # Skip complex $ref objects
            return None

        if prop.get("type") == "array":
            return None
        if prop.get("type") == "object":
            return None

        prop_type = prop.get("type", "string")
        prop_format = prop.get("format")

        # Inline enum
        if "enum" in prop:
            enum_type_name = snake_to_pascal(name)
            return Field(name, enum_type_name, is_enum=True,
                         enum_values=prop["enum"], required=required,
                         description=prop.get("description", ""),
                         is_id=is_id)

        java_type = TYPE_MAP.get((prop_type, prop_format),
                                  TYPE_MAP.get((prop_type, None), "String"))

        return Field(name, java_type, required=required,
                     description=prop.get("description", ""),
                     is_id=is_id)

    def _build_resources(self):
        """Group paths into resources."""
        resource_map: Dict[str, List[EndpointDef]] = {}

        for path, methods in self.paths.items():
            top_resource = path.strip("/").split("/")[0]
            if top_resource not in resource_map:
                resource_map[top_resource] = []

            for method_name in ("get", "post", "put", "patch", "delete"):
                if method_name not in methods:
                    continue
                op = methods[method_name]

                # Find response schema
                resp_code = "200"
                resp_schema = None
                for code in ("200", "201", "204"):
                    if code in op.get("responses", {}):
                        resp_code = code
                        content = op["responses"][code].get("content", {})
                        json_ct = content.get("application/json", {})
                        s = json_ct.get("schema", {})
                        if "$ref" in s:
                            resp_schema = resolve_ref(s["$ref"])
                        elif s.get("type") == "array" and "$ref" in s.get("items", {}):
                            resp_schema = resolve_ref(s["items"]["$ref"])
                        break

                # Find request schema
                req_schema = None
                rb = op.get("requestBody", {})
                if rb:
                    rc = rb.get("content", {}).get("application/json", {})
                    rs = rc.get("schema", {})
                    if "$ref" in rs:
                        req_schema = resolve_ref(rs["$ref"])

                # Path params
                path_params = []
                for p in op.get("parameters", []):
                    if isinstance(p, dict) and p.get("in") == "path":
                        path_params.append(p["name"])
                    elif isinstance(p, dict) and "$ref" in p:
                        ref_name = resolve_ref(p["$ref"])
                        param_def = self.parameters.get(ref_name, {})
                        if param_def.get("in") == "path":
                            path_params.append(param_def.get("name", ref_name))

                # Query params
                query_params = []
                for p in op.get("parameters", []):
                    if isinstance(p, dict) and p.get("in") == "query":
                        query_params.append({
                            "name": p["name"],
                            "type": p.get("schema", {}).get("type", "string"),
                            "format": p.get("schema", {}).get("format"),
                            "required": p.get("required", False),
                        })

                resource_map[top_resource].append(EndpointDef(
                    method=method_name.upper(),
                    path=path,
                    operation_id=op.get("operationId", ""),
                    summary=op.get("summary", ""),
                    response_code=resp_code,
                    response_schema=resp_schema,
                    request_schema=req_schema,
                    path_params=path_params,
                    query_params=query_params,
                ))

        # Map resources to entities
        for res_path, endpoints in resource_map.items():
            # Find matching entity by checking response schemas
            entity_name = None
            for ep in endpoints:
                if ep.response_schema and any(
                    e.name == ep.response_schema for e in self.entities
                ):
                    entity_name = ep.response_schema
                    break

            if not entity_name and self.entities:
                entity_name = self.entities[0].name

            self.resources.append(ResourceDef(
                base_path="/" + res_path,
                endpoints=endpoints,
                entity_name=entity_name,
            ))

    # --- File generation ---

    def generate(self) -> bool:
        """Generate the complete service project."""
        if self.svc_dir.exists():
            print(f"  SKIP {self.svc_name} (already exists)")
            return False

        print(f"  Generating {self.svc_name} ({len(self.entities)} entities, "
              f"{sum(len(r.endpoints) for r in self.resources)} endpoints)...")

        self.svc_dir.mkdir(parents=True)

        self._copy_template_files()
        self._write_settings_gradle()
        self._write_application_yaml()
        self._write_application_dev_yaml()
        self._write_application_class()

        for entity in self.entities:
            self._write_entity(entity)
            self._write_repository(entity)

        for resource in self.resources:
            self._write_controller(resource)

        self._write_flyway_migration()

        return True

    def _write(self, path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(content)

    def _java_dir(self, *sub) -> Path:
        return self.svc_dir / "src" / "main" / "java" / "com" / "novatrek" / self.pkg / Path(*sub)

    def _res_dir(self) -> Path:
        return self.svc_dir / "src" / "main" / "resources"

    def _copy_template_files(self):
        shutil.copy2(TEMPLATE_DIR / "build.gradle.kts",
                      self.svc_dir / "build.gradle.kts")
        shutil.copy2(TEMPLATE_DIR / "Dockerfile",
                      self.svc_dir / "Dockerfile")

        logback_src = TEMPLATE_DIR / "src" / "main" / "resources" / "logback-spring.xml"
        if logback_src.exists():
            dst = self._res_dir() / "logback-spring.xml"
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(logback_src, dst)

    def _write_settings_gradle(self):
        self._write(self.svc_dir / "settings.gradle.kts",
                     f'rootProject.name = "{self.svc_name}"\n')

    def _write_application_yaml(self):
        self._write(self._res_dir() / "application.yaml", f"""\
spring:
  application:
    name: {self.svc_name}

  datasource:
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: validate
    open-in-view: false
    properties:
      hibernate:
        default_schema: {self.db_schema}

  flyway:
    enabled: true
    schemas: {self.db_schema}
    clean-disabled: true
    baseline-on-migrate: true

  jackson:
    default-property-inclusion: non_null
    serialization:
      write-dates-as-timestamps: false

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
""")

    def _write_application_dev_yaml(self):
        self._write(self._res_dir() / "application-dev.yaml", """\
spring:
  config:
    activate:
      on-profile: dev

  datasource:
    url: jdbc:postgresql://${DATABASE_HOST}:5432/novatrek_dev
    hikari:
      maximum-pool-size: 10
      minimum-idle: 2

logging:
  level:
    com.novatrek: DEBUG
""")

    def _write_application_class(self):
        self._write(self._java_dir(f"{self.class_prefix}Application.java"), f"""\
package com.novatrek.{self.pkg};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class {self.class_prefix}Application {{
    public static void main(String[] args) {{
        SpringApplication.run({self.class_prefix}Application.class, args);
    }}
}}
""")

    def _write_entity(self, entity: EntityDef):
        imports = {
            "jakarta.persistence.*",
            "java.util.UUID",
            "java.time.OffsetDateTime",
        }
        for f in entity.fields:
            if f.java_type == "LocalDate":
                imports.add("java.time.LocalDate")
            elif f.java_type == "BigDecimal":
                imports.add("java.math.BigDecimal")

        lines = [
            f"package com.novatrek.{self.pkg}.entity;",
            "",
        ]
        for imp in sorted(imports):
            lines.append(f"import {imp};")
        lines.extend(["", "@Entity",
                       f'@Table(name = "{entity.table_name}", schema = "{self.db_schema}")',
                       f"public class {entity.name} {{", ""])

        # --- Fields ---
        # Standard fields we'll add at the end if not present in spec
        spec_field_names = {f.spec_name for f in entity.fields}
        has_created = "created_at" in spec_field_names or "createdAt" in spec_field_names
        has_updated = "updated_at" in spec_field_names or "updatedAt" in spec_field_names
        has_version = "version" in spec_field_names

        enums_to_declare = []

        for f in entity.fields:
            # Skip timestamp/version fields from spec — we add canonical versions below
            if f.spec_name in ("created_at", "updated_at", "version",
                                "createdAt", "updatedAt"):
                continue
            if f.spec_name.endswith("_at") and f.java_type == "OffsetDateTime":
                # enrolled_at, completed_at, etc. — keep these
                if f.spec_name not in ("created_at", "updated_at"):
                    pass
                else:
                    continue

            if f.is_id:
                lines.append("    @Id")
                lines.append("    @GeneratedValue(strategy = GenerationType.UUID)")
                lines.append(f'    @Column(name = "{f.col_name}")')
                lines.append(f"    private UUID {f.java_name};")
                lines.append("")
                continue

            if f.is_enum:
                lines.append("    @Enumerated(EnumType.STRING)")
                lines.append(f'    @Column(name = "{f.col_name}", length = 30)')
                lines.append(f"    private {f.java_type} {f.java_name};")
                lines.append("")
                enums_to_declare.append(f)
                continue

            # Regular field
            col_parts = [f'name = "{f.col_name}"']
            if f.required:
                col_parts.append("nullable = false")
            if f.java_type == "String":
                if any(kw in f.spec_name.lower() for kw in
                       ("description", "notes", "body", "content", "message")):
                    col_parts.append('columnDefinition = "TEXT"')
                elif any(kw in f.spec_name.lower() for kw in ("url", "image", "link")):
                    col_parts.append("length = 500")
                else:
                    col_parts.append("length = 255")
            if f.java_type == "BigDecimal":
                col_parts.append("precision = 10")
                col_parts.append("scale = 2")

            lines.append(f'    @Column({", ".join(col_parts)})')
            lines.append(f"    private {f.java_type} {f.java_name};")
            lines.append("")

        # Canonical timestamp + version fields
        lines.append('    @Column(name = "created_at", nullable = false, updatable = false)')
        lines.append("    private OffsetDateTime createdAt;")
        lines.append("")
        lines.append('    @Column(name = "updated_at", nullable = false)')
        lines.append("    private OffsetDateTime updatedAt;")
        lines.append("")
        lines.append("    @Version")
        lines.append('    @Column(name = "version")')
        lines.append("    private Integer version = 0;")
        lines.append("")

        # PrePersist / PreUpdate
        lines.extend([
            "    @PrePersist",
            "    protected void onCreate() {",
            "        createdAt = OffsetDateTime.now();",
            "        updatedAt = OffsetDateTime.now();",
            "    }",
            "",
            "    @PreUpdate",
            "    protected void onUpdate() {",
            "        updatedAt = OffsetDateTime.now();",
            "    }",
            "",
        ])

        # Enum declarations
        for f in enums_to_declare:
            vals = ", ".join(f.enum_values)
            lines.append(f"    public enum {f.java_type} {{ {vals} }}")
        if enums_to_declare:
            lines.append("")

        # Getters and Setters
        lines.append("    // --- Getters and Setters ---")
        lines.append("")

        for f in entity.fields:
            if f.spec_name in ("created_at", "updated_at", "version",
                                "createdAt", "updatedAt"):
                continue
            pascal = f.java_name[0].upper() + f.java_name[1:]
            jt = "UUID" if f.is_id else f.java_type
            lines.append(f"    public {jt} get{pascal}() {{ return {f.java_name}; }}")
            lines.append(f"    public void set{pascal}({jt} {f.java_name}) "
                          f"{{ this.{f.java_name} = {f.java_name}; }}")
            lines.append("")

        # Standard getters
        lines.extend([
            "    public OffsetDateTime getCreatedAt() { return createdAt; }",
            "    public OffsetDateTime getUpdatedAt() { return updatedAt; }",
            "    public Integer getVersion() { return version; }",
            "    public void setVersion(Integer version) { this.version = version; }",
            "}",
            "",
        ])

        self._write(self._java_dir("entity", f"{entity.name}.java"), "\n".join(lines))

    def _write_repository(self, entity: EntityDef):
        self._write(self._java_dir("repository", f"{entity.name}Repository.java"), f"""\
package com.novatrek.{self.pkg}.repository;

import com.novatrek.{self.pkg}.entity.{entity.name};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface {entity.name}Repository extends JpaRepository<{entity.name}, UUID> {{
}}
""")

    def _write_controller(self, resource: ResourceDef):
        """Generate a controller class for a resource group."""
        entity = next((e for e in self.entities if e.name == resource.entity_name), None)
        if not entity:
            return

        repo_name = f"{entity.name}Repository"
        repo_var = entity.name[0].lower() + entity.name[1:] + "Repository"
        entity_var = entity.name[0].lower() + entity.name[1:]

        # Find the ID field
        id_field = next((f for f in entity.fields if f.is_id), None)
        id_param = id_field.java_name if id_field else "id"
        id_path_name = id_field.col_name if id_field else "id"

        # Determine patchable fields (non-id, non-timestamp, non-version)
        skip_patch = {id_field.spec_name if id_field else "id",
                      "created_at", "updated_at", "version",
                      "createdAt", "updatedAt"}
        patchable = [f for f in entity.fields if f.spec_name not in skip_patch
                     and f.java_type != "OffsetDateTime"]

        lines = [
            f"package com.novatrek.{self.pkg}.controller;",
            "",
            f"import com.novatrek.{self.pkg}.entity.{entity.name};",
            f"import com.novatrek.{self.pkg}.repository.{repo_name};",
            "import jakarta.validation.Valid;",
            "import org.springframework.http.HttpStatus;",
            "import org.springframework.http.ResponseEntity;",
            "import org.springframework.web.bind.annotation.*;",
            "import org.springframework.web.server.ResponseStatusException;",
            "",
            "import java.util.List;",
            "import java.util.UUID;",
            "",
            "@RestController",
            f'@RequestMapping("{resource.base_path}")',
            f"public class {resource.controller_name} {{",
            "",
            f"    private final {repo_name} {repo_var};",
            "",
            f"    public {resource.controller_name}({repo_name} {repo_var}) {{",
            f"        this.{repo_var} = {repo_var};",
            "    }",
            "",
        ]

        # Generate endpoint methods
        for ep in resource.endpoints:
            rel_path = ep.path[len(resource.base_path):] if ep.path.startswith(resource.base_path) else ep.path
            if not rel_path:
                rel_path = ""

            # Convert {param_name} to Spring {paramName}
            spring_path = rel_path
            for pp in ep.path_params:
                camel_pp = snake_to_camel(pp)
                spring_path = spring_path.replace(f"{{{pp}}}", f"{{{camel_pp}}}")

            method_name = ep.operation_id or f"{ep.method.lower()}{snake_to_pascal(rel_path.replace('/', '_').replace('{', '').replace('}', ''))}"

            # Annotation
            ann_map = {"GET": "GetMapping", "POST": "PostMapping",
                       "PUT": "PutMapping", "PATCH": "PatchMapping",
                       "DELETE": "DeleteMapping"}
            ann = ann_map.get(ep.method, "GetMapping")
            path_arg = f'("{spring_path}")' if spring_path else ""

            lines.append(f"    @{ann}{path_arg}")

            # Method signature
            params = []
            for pp in ep.path_params:
                camel_pp = snake_to_camel(pp)
                params.append(f"@PathVariable UUID {camel_pp}")

            if ep.request_schema:
                params.append(f"@Valid @RequestBody {entity.name} body")

            # Determine return type
            if ep.method == "DELETE":
                ret_type = "ResponseEntity<Void>"
            elif ep.response_code == "201":
                ret_type = f"ResponseEntity<{entity.name}>"
            elif ep.method == "GET" and not ep.path_params:
                ret_type = f"List<{entity.name}>"
            else:
                ret_type = entity.name

            param_str = ", ".join(params)
            lines.append(f"    public {ret_type} {method_name}({param_str}) {{")

            # Method body
            if ep.method == "GET" and not ep.path_params:
                # List
                lines.append(f"        return {repo_var}.findAll();")
            elif ep.method == "GET" and ep.path_params:
                # Get by ID
                pp = snake_to_camel(ep.path_params[0])
                lines.extend([
                    f"        return {repo_var}.findById({pp})",
                    f'                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "{entity.name} not found"));',
                ])
            elif ep.method == "POST" and ep.response_code == "201":
                # Create
                lines.extend([
                    f"        {entity.name} saved = {repo_var}.save(body);",
                    f"        return ResponseEntity.status(HttpStatus.CREATED).body(saved);",
                ])
            elif ep.method == "POST" and ep.path_params:
                # Action on resource (e.g., gear-verification, wristband-assignment)
                pp = snake_to_camel(ep.path_params[0])
                lines.extend([
                    f"        {entity.name} existing = {repo_var}.findById({pp})",
                    f'                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "{entity.name} not found"));',
                    f"        return {repo_var}.save(existing);",
                ])
            elif ep.method == "PATCH" and ep.path_params:
                # Partial update
                pp = snake_to_camel(ep.path_params[0])
                lines.extend([
                    f"        {entity.name} existing = {repo_var}.findById({pp})",
                    f'                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "{entity.name} not found"));',
                    "",
                ])
                for pf in patchable:
                    pascal = pf.java_name[0].upper() + pf.java_name[1:]
                    lines.append(f"        if (body.get{pascal}() != null) existing.set{pascal}(body.get{pascal}());")
                lines.append("")
                lines.append(f"        return {repo_var}.save(existing);")
            elif ep.method == "PUT" and ep.path_params:
                # Status transition or full update
                pp = snake_to_camel(ep.path_params[0])
                lines.extend([
                    f"        {entity.name} existing = {repo_var}.findById({pp})",
                    f'                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "{entity.name} not found"));',
                    f"        return {repo_var}.save(existing);",
                ])
            elif ep.method == "DELETE" and ep.path_params:
                pp = snake_to_camel(ep.path_params[0])
                lines.extend([
                    f"        if (!{repo_var}.existsById({pp})) {{",
                    f'            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "{entity.name} not found");',
                    "        }",
                    f"        {repo_var}.deleteById({pp});",
                    "        return ResponseEntity.noContent().build();",
                ])
            else:
                # Fallback
                lines.append(f"        throw new UnsupportedOperationException(\"Not yet implemented\");")

            lines.extend(["    }", ""])

        lines.extend(["}", ""])

        self._write(self._java_dir("controller", f"{resource.controller_name}.java"),
                     "\n".join(lines))

    def _write_flyway_migration(self):
        """Generate V1__baseline.sql from entities."""
        lines = [f"CREATE SCHEMA IF NOT EXISTS {self.db_schema};", ""]

        for entity in self.entities:
            lines.append(f"CREATE TABLE {self.db_schema}.{entity.table_name} (")
            col_lines = []

            id_field = next((f for f in entity.fields if f.is_id), None)
            if id_field:
                col_lines.append(
                    f"    {id_field.col_name:30s} UUID PRIMARY KEY DEFAULT gen_random_uuid()")

            for f in entity.fields:
                if f.is_id:
                    continue
                if f.spec_name in ("created_at", "updated_at", "version",
                                    "createdAt", "updatedAt"):
                    continue

                sql_type = SQL_TYPE_MAP.get(f.java_type, "VARCHAR(255)")
                if f.is_enum:
                    sql_type = "VARCHAR(30)"
                elif f.java_type == "String":
                    if any(kw in f.spec_name.lower() for kw in
                           ("description", "notes", "body", "content", "message")):
                        sql_type = "TEXT"
                    elif any(kw in f.spec_name.lower() for kw in ("url", "image", "link")):
                        sql_type = "VARCHAR(500)"

                nullable = "" if f.required else ""
                not_null = " NOT NULL" if f.required else ""
                col_lines.append(f"    {f.col_name:30s} {sql_type}{not_null}")

            # Standard columns
            col_lines.append(f"    {'created_at':30s} TIMESTAMPTZ   NOT NULL DEFAULT NOW()")
            col_lines.append(f"    {'updated_at':30s} TIMESTAMPTZ   NOT NULL DEFAULT NOW()")
            col_lines.append(f"    {'version':30s} INTEGER       NOT NULL DEFAULT 0")

            lines.append(",\n".join(col_lines))
            lines.extend([");", ""])

        migration_dir = self._res_dir() / "db" / "migration"
        self._write(migration_dir / "V1__baseline.sql", "\n".join(lines))


def main():
    specs = sorted(SPECS_DIR.glob("svc-*.yaml"))

    if "--list" in sys.argv:
        print("Services to generate:")
        for spec in specs:
            svc = spec.stem
            status = "EXISTS" if svc in EXISTING_SERVICES or (SERVICES_DIR / svc).exists() else "NEW"
            print(f"  {svc:40s} [{status}]")
        return

    # Filter to specific service if provided
    target = None
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            target = arg

    generated = 0
    skipped = 0

    for spec in specs:
        svc = spec.stem
        if svc in EXISTING_SERVICES:
            skipped += 1
            continue
        if target and svc != target:
            continue

        gen = ServiceGenerator(spec)
        if gen.generate():
            generated += 1
        else:
            skipped += 1

    print(f"\nDone: {generated} generated, {skipped} skipped")


if __name__ == "__main__":
    main()
