#!/bin/bash

# This script performs a basic health check on the API endpoints.

# Color definitions
C_RESET=$(tput sgr0)
C_GREEN=$(tput setaf 2)
C_RED=$(tput setaf 1)
C_BLUE=$(tput setaf 4)

log_info() { echo -e "${C_BLUE}TEST:${C_RESET} $1"; }
log_success() { echo -e "${C_GREEN}PASS:${C_RESET} $1"; }
log_fail() { echo -e "${C_RED}FAIL:${C_RESET} $1"; }

BASE_URL=$1
if [ -z "$BASE_URL" ]; then
    echo "Usage: $0 <base_url>"
    exit 1
fi

log_info "Starting API health checks for $BASE_URL..."

# Test 1: Check the frontend endpoint (should return 200 OK)
log_info "Checking frontend accessibility..."
status_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL")
if [ "$status_code" -eq 200 ]; then
    log_success "Frontend is accessible (Status: $status_code)."
else
    log_fail "Frontend check failed (Status: $status_code)."
fi

# Test 2: Check a known API endpoint. /api/register/ should return 405 for a GET request.
log_info "Checking a backend API endpoint (/api/register/)..."
api_status_code=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/api/register/")
if [ "$api_status_code" -eq 405 ]; then
    log_success "Backend API is responding as expected (Status: $api_status_code)."
else
    log_fail "Backend API check failed. Expected 405, but got $api_status_code."
fi

log_info "API health check complete."