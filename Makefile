# Project Chimera - Makefile for automation
# Provides common development and CI/CD commands

.PHONY: setup test build spec-check clean help

# Docker image name and tag
IMAGE_NAME := chimera-fde
IMAGE_TAG := latest

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Project Chimera - Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Install local dependencies using uv
	@echo "Installing dependencies with uv..."
	uv sync

test: build ## Run pytest tests in Docker container
	@echo "Running tests in Docker..."
	docker run --rm $(IMAGE_NAME):$(IMAGE_TAG) uv run pytest tests/ -v

build: ## Build Docker image
	@echo "Building Docker image: $(IMAGE_NAME):$(IMAGE_TAG)"
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

spec-check: ## Verify code references specs/ and SRS terms
	@echo "Checking spec alignment..."
	@./scripts/spec-check.sh

clean: ## Remove Docker image and local build artifacts
	@echo "Cleaning up..."
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true
	rm -rf .venv __pycache__ .pytest_cache *.egg-info 2>/dev/null || true
