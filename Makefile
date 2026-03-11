# ===========================================================================
# NovaTrek Adventures — Makefile
# ===========================================================================
# Quick commands for local development, building, and deployment.
# ===========================================================================

.PHONY: help dev-up dev-down dev-reset build test deploy-dev deploy-prod \
        what-if-dev what-if-prod portal-build portal-serve lint \
        confluence-prepare confluence-publish-dry-run confluence-publish \
        confluence-verify confluence-lock confluence-drift-check confluence-wipe \
        confluence-full

# Default target
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ===========================================================================
# Local Development
# ===========================================================================

dev-up: ## Start local PostgreSQL + Redis (Docker Compose)
	docker compose up -d
	@echo ""
	@echo "PostgreSQL: localhost:5432 (novatrekadmin/localdev123)"
	@echo "Redis:      localhost:6379"

dev-down: ## Stop local services
	docker compose down

dev-reset: ## Stop and remove all data volumes
	docker compose down -v

dev-logs: ## Tail local service logs
	docker compose logs -f

# ===========================================================================
# Infrastructure
# ===========================================================================

what-if-dev: ## Preview dev infrastructure changes (no deploy)
	./infra/deploy-platform.sh dev --what-if

what-if-prod: ## Preview prod infrastructure changes (no deploy)
	./infra/deploy-platform.sh prod --what-if

deploy-dev: ## Deploy dev infrastructure
	./infra/deploy-platform.sh dev

deploy-prod: ## Deploy prod infrastructure
	./infra/deploy-platform.sh prod

teardown-dev: ## Destroy dev environment (interactive confirmation)
	./infra/deploy-platform.sh dev --teardown

# ===========================================================================
# Portal
# ===========================================================================

portal-build: ## Build architecture portal (MkDocs)
	cd portal && python3 -m mkdocs build

portal-serve: ## Serve architecture portal locally
	cd portal && python3 -m mkdocs serve

portal-generate: ## Regenerate all portal pages from metadata
	bash portal/scripts/generate-all.sh

# ===========================================================================
# Bicep
# ===========================================================================

lint: ## Lint all Bicep files
	az bicep build --file infra/platform.bicep --stdout > /dev/null
	az bicep build --file infra/main.bicep --stdout > /dev/null
	@echo "Bicep lint passed."

# ===========================================================================
# Service Operations (requires service name: make SVC=svc-check-in ...)
# ===========================================================================

svc-build: ## Build a service: make svc-build SVC=svc-check-in
	cd services/$(SVC) && ./gradlew build

svc-test: ## Test a service: make svc-test SVC=svc-check-in
	cd services/$(SVC) && ./gradlew test

svc-run: ## Run a service locally: make svc-run SVC=svc-check-in
	cd services/$(SVC) && SPRING_PROFILES_ACTIVE=local ./gradlew bootRun

svc-docker: ## Build Docker image: make svc-docker SVC=svc-check-in
	docker build -t novatrek/$(SVC):latest services/$(SVC)

svc-health: ## Check service health in dev: make svc-health SVC=svc-check-in
	@FQDN=$$(az containerapp show -n ca-$(SVC) -g rg-novatrek-dev \
		--query "properties.configuration.ingress.fqdn" -o tsv 2>/dev/null) && \
	curl -s "https://$${FQDN}/actuator/health" | python3 -m json.tool

svc-logs: ## Tail service logs in dev: make svc-logs SVC=svc-check-in
	az containerapp logs show -n ca-$(SVC) -g rg-novatrek-dev --follow

# ===========================================================================
# Confluence Publishing
# ===========================================================================

confluence-prepare: ## Generate Confluence staging from portal docs
	python3 portal/scripts/confluence-prepare.py

confluence-publish-dry-run: ## Dry-run publish to Confluence (validate only)
	python3 portal/scripts/confluence-prepare.py
	mark --ci --base-url "$$CONFLUENCE_BASE_URL" \
		-u "$$CONFLUENCE_USERNAME" -p "$$CONFLUENCE_API_TOKEN" \
		-f "portal/confluence/**/*.md" --dry-run

confluence-publish: ## Publish portal docs to Confluence
	python3 portal/scripts/confluence-prepare.py
	mark --ci --base-url "$$CONFLUENCE_BASE_URL" \
		-u "$$CONFLUENCE_USERNAME" -p "$$CONFLUENCE_API_TOKEN" \
		-f "portal/confluence/**/*.md"

confluence-verify: ## Verify published Confluence content matches staging
	python3 portal/scripts/confluence-verify.py \
		--base-url "$$CONFLUENCE_BASE_URL" \
		--username "$$CONFLUENCE_USERNAME" \
		--api-token "$$CONFLUENCE_API_TOKEN" \
		--space "$$CONFLUENCE_SPACE"

confluence-lock: ## Lock auto-generated Confluence pages
	python3 portal/scripts/confluence-lock-pages.py \
		--base-url "$$CONFLUENCE_BASE_URL" \
		--username "$$CONFLUENCE_USERNAME" \
		--api-token "$$CONFLUENCE_API_TOKEN" \
		--space "$$CONFLUENCE_SPACE" \
		--label "auto-generated"

confluence-drift-check: ## Check for unauthorized edits in Confluence
	python3 portal/scripts/confluence-drift-check.py \
		--staging-dir portal/confluence

confluence-wipe: ## Delete all pages from Confluence space (DANGEROUS)
	@echo "WARNING: This will delete ALL pages from the ARCH space!"
	@read -p "Type WIPE to confirm: " confirm && [ "$$confirm" = "WIPE" ] || exit 1
	python3 portal/scripts/confluence-delete-space-content.py \
		--base-url "$$CONFLUENCE_BASE_URL" \
		--username "$$CONFLUENCE_USERNAME" \
		--api-token "$$CONFLUENCE_API_TOKEN" \
		--space "$$CONFLUENCE_SPACE"

confluence-full: ## Full cycle: prepare -> publish -> verify -> lock
	$(MAKE) confluence-publish
	$(MAKE) confluence-verify
	$(MAKE) confluence-lock
