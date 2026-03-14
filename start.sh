#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# Rig Tools · Docker Startup Script
# Usage: bash start.sh [--build] [--down] [--logs]
# ──────────────────────────────────────────────────────────────────────────────

set -euo pipefail

COMPOSE_FILE="docker/docker-compose.yml"
ENV_FILE="docker/.env"
ENV_EXAMPLE="docker/.env.example"

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

info()    { echo -e "${BLUE}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; }

# ── Header ────────────────────────────────────────────────────────────────────
echo -e ""
echo -e "${BOLD}  🛢️  Rig Tools${RESET}"
echo -e "  ─────────────────────────────────"
echo -e ""

# ── Parse flags ───────────────────────────────────────────────────────────────
BUILD_FLAG=""
case "${1:-}" in
    --build)  BUILD_FLAG="--build" ;;
    --down)
        info "Stopping all services..."
        docker compose -f "$COMPOSE_FILE" down
        success "Services stopped."
        exit 0
        ;;
    --logs)
        docker compose -f "$COMPOSE_FILE" logs -f
        exit 0
        ;;
esac

# ── Preflight checks ──────────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
    error "Docker is not installed. Install it from https://docs.docker.com/get-docker/"
    exit 1
fi

if ! docker info &>/dev/null; then
    error "Docker daemon is not running. Start Docker Desktop and try again."
    exit 1
fi
success "Docker is running"

# ── Environment file ──────────────────────────────────────────────────────────
if [ ! -f "$ENV_FILE" ]; then
    warn ".env not found. Creating from example..."
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    warn "Review ${ENV_FILE} and set SECRET_KEY before production use."
fi

# ── Create volume directories ─────────────────────────────────────────────────
info "Ensuring data directories..."
mkdir -p data
success "data/ ready"

# ── Start services ────────────────────────────────────────────────────────────
info "Starting services (this may take a minute on first run)..."
echo ""
docker compose -f "$COMPOSE_FILE" up $BUILD_FLAG -d

# ── Wait for health ───────────────────────────────────────────────────────────
echo ""
info "Waiting for API health check..."
MAX_WAIT=60
ELAPSED=0
until curl -sf http://localhost:8000/api/health > /dev/null; do
    if [ $ELAPSED -ge $MAX_WAIT ]; then
        error "API did not become healthy within ${MAX_WAIT}s."
        error "Check logs with: bash start.sh --logs"
        exit 1
    fi
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done
success "API is healthy"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}  ✅  Rig Tools is running${RESET}"
echo -e "  ─────────────────────────────────"
echo -e "  ${GREEN}Frontend${RESET}   http://localhost:8501"
echo -e "  ${GREEN}API${RESET}        http://localhost:8000"
echo -e "  ${GREEN}API Docs${RESET}   http://localhost:8000/docs"
echo ""
echo -e "  ${BOLD}Useful commands:${RESET}"
echo -e "    bash start.sh --build    Rebuild images and restart"
echo -e "    bash start.sh --logs     Follow service logs"
echo -e "    bash start.sh --down     Stop all services"
echo -e "    docker compose -f docker/docker-compose.yml ps"
echo ""
