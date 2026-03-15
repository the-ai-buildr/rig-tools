# Rig Tools — Makefile
# All Docker commands use docker/docker-compose.yml (single-service, port 8501).
#
# Usage:
#   make          → show help
#   make dev      → start app (build if needed)
#   make build    → rebuild image and restart
#   make down     → stop and remove containers
#   make logs     → follow container logs
#   make ps       → show container status
#   make health   → hit the health endpoint
#   make shell    → exec bash inside the running container
#   make test     → run test suite locally (no Docker)
#   make clean    → remove stopped containers + dangling images

COMPOSE      := docker compose -f docker/docker-compose.yml
ENV_FILE     := docker/.env
ENV_EXAMPLE  := docker/.env.example
APP_URL      := http://localhost:8501
HEALTH_URL   := $(APP_URL)/api/health

# ── Colours ───────────────────────────────────────────────────────────────────
BOLD  := \033[1m
GREEN := \033[0;32m
RESET := \033[0m

.DEFAULT_GOAL := help

# ── Help ──────────────────────────────────────────────────────────────────────
.PHONY: help
help:
	@echo ""
	@echo "  $(BOLD)🛢  Rig Tools$(RESET)"
	@echo "  ─────────────────────────────────────────────────────"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make dev"     "Start app in background (builds on first run)"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make build"   "Force-rebuild image and restart"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make down"    "Stop and remove containers"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make restart" "down + dev"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make logs"    "Follow live container logs"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make ps"      "Show running containers"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make health"  "Check /api/health endpoint"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make shell"   "Open bash inside running container"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make test"    "Run test suite locally (fast, no Docker)"
	@printf "  $(BOLD)%-14s$(RESET) %s\n" "make clean"   "Remove stopped containers + dangling images"
	@echo ""

# ── Environment guard ─────────────────────────────────────────────────────────
$(ENV_FILE):
	@echo "  [WARN] $(ENV_FILE) not found — copying from example..."
	@cp $(ENV_EXAMPLE) $(ENV_FILE)
	@echo "  [WARN] Review $(ENV_FILE) and set SECRET_KEY before production use."

# ── Docker targets ────────────────────────────────────────────────────────────
.PHONY: dev
dev: $(ENV_FILE)
	@mkdir -p data
	$(COMPOSE) up -d
	@echo ""
	@echo "  $(GREEN)App$(RESET)        $(APP_URL)"
	@echo "  $(GREEN)API Docs$(RESET)   $(APP_URL)/api/docs"
	@echo "  $(GREEN)API Health$(RESET) $(HEALTH_URL)"
	@echo ""
	@echo "  Run 'make logs' to follow output or 'make health' to verify."

.PHONY: build
build: $(ENV_FILE)
	@mkdir -p data
	$(COMPOSE) up -d --build
	@echo ""
	@echo "  $(GREEN)Rebuilt and started.$(RESET)"
	@echo "  $(GREEN)App$(RESET)        $(APP_URL)"

.PHONY: down
down:
	$(COMPOSE) down
	@echo "  Stopped."

.PHONY: restart
restart: down dev

.PHONY: logs
logs:
	$(COMPOSE) logs -f

.PHONY: ps
ps:
	$(COMPOSE) ps

.PHONY: health
health:
	@echo "  Checking $(HEALTH_URL)..."
	@curl -sf $(HEALTH_URL) | python3 -m json.tool && echo "" || \
	  (echo "  [ERROR] Health check failed — is the app running? Try 'make dev'" && exit 1)

.PHONY: shell
shell:
	$(COMPOSE) exec app bash

.PHONY: clean
clean:
	$(COMPOSE) down --remove-orphans
	docker image prune -f
	@echo "  Cleaned."

# ── Test target (local, no Docker) ────────────────────────────────────────────
.PHONY: test
test:
	@echo "  Running test suite..."
	PYTHONPATH=src python3 -m pytest tests/ -v --tb=short
