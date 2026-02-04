#!/bin/bash
# OpenClaw One-Click Installation Script
# Usage: ./install.sh [--docker|--npm|--dev]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Default installation method
INSTALL_METHOD="${1:-npm}"

echo "============================================"
echo "  OpenClaw Installation Script"
echo "  Method: $INSTALL_METHOD"
echo "============================================"

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        log_error "Node.js 18+ required. Current: $(node -v)"
        exit 1
    fi
    
    log_info "Node.js version: $(node -v) ✓"
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        log_error "npm is not installed."
        exit 1
    fi
    log_info "npm version: $(npm -v) ✓"
}

# Install via npm
install_npm() {
    log_info "Installing OpenClaw via npm..."
    npm install -g openclaw@latest
    
    log_info "Running onboard setup..."
    openclaw onboard --install-daemon
    
    log_info "Installation complete!"
}

# Install via Docker
install_docker() {
    log_info "Installing OpenClaw via Docker..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Create docker-compose.yml if not exists
    if [ ! -f "configs/docker-compose.yml" ]; then
        log_error "docker-compose.yml not found in configs/"
        exit 1
    fi
    
    cd configs
    docker compose up -d openclaw-gateway
    
    log_info "Docker installation complete!"
    log_info "Check logs: docker compose logs -f openclaw-gateway"
}

# Health check
health_check() {
    log_info "Running health check..."
    
    if command -v openclaw &> /dev/null; then
        openclaw doctor || true
        openclaw health || true
    else
        log_warn "OpenClaw CLI not found in PATH"
    fi
}

# Main
main() {
    check_prerequisites
    
    case "$INSTALL_METHOD" in
        --npm|npm)
            install_npm
            ;;
        --docker|docker)
            install_docker
            ;;
        --dev|dev)
            log_info "Development mode - skipping installation"
            ;;
        *)
            log_error "Unknown method: $INSTALL_METHOD"
            echo "Usage: ./install.sh [--docker|--npm|--dev]"
            exit 1
            ;;
    esac
    
    health_check
    
    echo ""
    echo "============================================"
    echo "  Installation Complete!"
    echo "============================================"
    echo ""
    echo "Next steps:"
    echo "  1. Configure API keys: export ANTHROPIC_API_KEY=..."
    echo "  2. Start gateway: openclaw gateway --port 18789"
    echo "  3. Login to channels: openclaw channels login"
    echo ""
}

main "$@"
