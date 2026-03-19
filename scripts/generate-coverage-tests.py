#!/usr/bin/env python3
"""Generate coverage-boosting PATCH test methods for all NovaTrek services.

Scans each service's controllers for PATCH methods with null-check branches,
then appends additional test methods to existing controller test files to
cover both the 'all fields set' and 'not found' branches.
"""
import os
import re
import sys

SERVICES_DIR = os.path.join(os.path.dirname(__file__), '..', 'services')

# Map: service -> list of (controller_file, entity, patch_path, fields)
# We auto-discover from source

def find_patch_info(svc_dir):
    """Find controllers with PATCH methods and their field null-checks."""
    results = []
    main_java = os.path.join(svc_dir, 'src', 'main', 'java')
    if not os.path.isdir(main_java):
        return results
    
    for root, dirs, files in os.walk(main_java):
        for f in files:
            if not f.endswith('Controller.java'):
                continue
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            
            # Find PATCH methods
            patch_match = re.search(r'@PatchMapping\("(/[^"]+)"\)', content)
            if not patch_match:
                continue
            
            patch_path = patch_match.group(1)
            
            # Find the RequestMapping base path
            base_match = re.search(r'@RequestMapping\("(/[^"]+)"\)', content)
            base_path = base_match.group(1) if base_match else ''
            
            # Find all null-check fields
            fields = re.findall(r'if \(body\.get(\w+)\(\) != null\)', content)
            
            # Find entity type from method signature
            entity_match = re.search(r'@RequestBody\s+(?:@Valid\s+)?(\w+)\s+body', content)
            entity_type = entity_match.group(1) if entity_match else None
            
            # Find the repository being used
            repo_match = re.search(r'private final (\w+Repository)\s+(\w+)', content)
            repo_type = repo_match.group(1) if repo_match else None
            repo_name = repo_match.group(2) if repo_match else None
            
            # Find the path variable name
            pathvar_match = re.search(r'@PathVariable\s+\w+\s+(\w+)', content)
            pathvar = pathvar_match.group(1) if pathvar_match else 'id'
            
            results.append({
                'controller_file': f,
                'controller_name': f.replace('.java', ''),
                'base_path': base_path,
                'patch_path': patch_path,
                'fields': fields,
                'entity_type': entity_type,
                'repo_type': repo_type,
                'repo_name': repo_name,
                'pathvar': pathvar,
            })
    
    return results


def find_existing_test(svc_dir, controller_name):
    """Find the test file for a controller."""
    test_java = os.path.join(svc_dir, 'src', 'test', 'java')
    if not os.path.isdir(test_java):
        return None
    for root, dirs, files in os.walk(test_java):
        for f in files:
            if f == controller_name + 'Test.java':
                return os.path.join(root, f)
    return None


def generate_setter_line(field, entity_type):
    """Generate a setter call with appropriate test value."""
    lower = field[0].lower() + field[1:]
    
    # Heuristic for types based on field name
    if lower.endswith('Id') or lower == 'id':
        return f'        patch.set{field}(UUID.randomUUID());'
    elif lower.endswith('Date') or lower.endswith('At'):
        if 'Local' in field or 'date' in lower.lower():
            return f'        patch.set{field}(java.time.LocalDate.of(2026, 1, 1));'
        else:
            return f'        patch.set{field}(java.time.OffsetDateTime.now());'
    elif lower.endswith('Amount') or lower.endswith('Rate') or lower.endswith('Total') or lower == 'mileage':
        return f'        patch.set{field}(java.math.BigDecimal.ONE);'
    elif lower.endswith('Count') or lower == 'capacity' or lower == 'radiusMeters' or lower == 'helpfulCount':
        return f'        patch.set{field}(1);'
    elif lower == 'rev':
        return f'        patch.set{field}(1);'
    elif lower.endswith('Required'):
        return f'        patch.set{field}(true);'
    else:
        return f'        patch.set{field}("{lower}-test-val");'


def generate_test_methods(info):
    """Generate allFields + notFound test methods."""
    entity = info['entity_type']
    base = info['base_path']
    patch_rel = info['patch_path']  # e.g., /{emergencyId}
    pathvar = info['pathvar']
    full_path = base + patch_rel
    
    setters = '\n'.join(generate_setter_line(f, entity) for f in info['fields'])
    
    methods = f'''
    @Test
    void update_allFields() throws Exception {{
        {entity} existing = new {entity}();
        UUID id = UUID.randomUUID();
        when({info['repo_name']}.findById(id)).thenReturn(Optional.of(existing));
        when({info['repo_name']}.save(any({entity}.class))).thenReturn(existing);

        {entity} patch = new {entity}();
{setters}

        mockMvc.perform(patch("{base}/{{{pathvar}}}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(patch)))
                .andExpect(status().isOk());
    }}

    @Test
    void update_notFound_returns404() throws Exception {{
        UUID id = UUID.randomUUID();
        when({info['repo_name']}.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("{base}/{{{pathvar}}}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(new {entity}())))
                .andExpect(status().isNotFound());
    }}'''
    
    return methods


def has_test_method(test_content, method_name):
    """Check if a test method already exists."""
    return f'void {method_name}(' in test_content


def add_tests_to_file(test_path, new_methods):
    """Insert new test methods before the final closing brace."""
    with open(test_path) as f:
        content = f.read()
    
    # Find the last closing brace (class end)
    last_brace = content.rfind('}')
    if last_brace == -1:
        return False
    
    # Check needed imports
    imports_needed = []
    if 'java.math.BigDecimal' not in content and 'BigDecimal' in new_methods:
        imports_needed.append('import java.math.BigDecimal;')
    if 'java.time.LocalDate' not in content and 'LocalDate.of' in new_methods:
        imports_needed.append('import java.time.LocalDate;')
    if 'java.time.OffsetDateTime' not in content and 'OffsetDateTime.now' in new_methods:
        imports_needed.append('import java.time.OffsetDateTime;')
    
    if imports_needed:
        # Add imports after the last existing import
        import_pos = content.rfind('\nimport ')
        if import_pos >= 0:
            end_of_import_line = content.index('\n', import_pos + 1)
            import_block = '\n'.join(imports_needed)
            content = content[:end_of_import_line + 1] + import_block + '\n' + content[end_of_import_line + 1:]
            # Recalculate last brace position
            last_brace = content.rfind('}')
    
    new_content = content[:last_brace] + new_methods + '\n}\n'
    
    with open(test_path, 'w') as f:
        f.write(new_content)
    
    return True


def main():
    services_dir = os.path.abspath(SERVICES_DIR)
    
    updated = 0
    skipped = 0
    
    for svc_name in sorted(os.listdir(services_dir)):
        svc_dir = os.path.join(services_dir, svc_name)
        if not os.path.isdir(svc_dir) or not svc_name.startswith('svc-'):
            continue
        
        patches = find_patch_info(svc_dir)
        if not patches:
            continue
        
        for info in patches:
            test_path = find_existing_test(svc_dir, info['controller_name'])
            if not test_path:
                print(f"  SKIP: No test file for {info['controller_name']}")
                skipped += 1
                continue
            
            with open(test_path) as f:
                test_content = f.read()
            
            if has_test_method(test_content, 'update_allFields'):
                print(f"  SKIP: {svc_name}/{info['controller_name']} already has allFields test")
                skipped += 1
                continue
            
            methods = generate_test_methods(info)
            if add_tests_to_file(test_path, methods):
                print(f"  ADDED: {svc_name}/{info['controller_name']}Test.java")
                updated += 1
            else:
                print(f"  ERROR: Could not update {test_path}")
    
    print(f"\nDone: {updated} updated, {skipped} skipped")


if __name__ == '__main__':
    main()
