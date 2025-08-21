#!/bin/bash

# Azure Cosmos DB vNext Docker Emulator Startup Script
# This script starts the Azure Cosmos DB vNext emulator in Docker
# Documentation: https://learn.microsoft.com/en-us/azure/cosmos-db/emulator-linux

set -e  # Exit on any error

# Configuration
CONTAINER_NAME="cosmos-emulator-vnext"
IMAGE_NAME="mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator:vnext-preview"
COSMOS_PORT="8081"
EXPLORER_PORT="1234"
PROTOCOL="https"  # Use HTTPS for .NET/Java SDK compatibility
LOG_LEVEL="info"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Azure Cosmos DB vNext Emulator Startup Script ===${NC}"
echo -e "${BLUE}Documentation: https://learn.microsoft.com/en-us/azure/cosmos-db/emulator-linux${NC}"
echo ""

# Function to check if Docker is running
check_docker() {
    echo -e "${YELLOW}Checking if Docker is running...${NC}"
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker Desktop and try again.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to check if container already exists
check_existing_container() {
    if docker ps -a --filter "name=${CONTAINER_NAME}" --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        echo -e "${YELLOW}⚠️  Container '${CONTAINER_NAME}' already exists${NC}"
        read -p "Do you want to remove the existing container and start fresh? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Removing existing container...${NC}"
            docker rm -f "${CONTAINER_NAME}" || true
        else
            echo -e "${YELLOW}Checking if container is running...${NC}"
            if docker ps --filter "name=${CONTAINER_NAME}" --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
                echo -e "${GREEN}✅ Container is already running${NC}"
                show_connection_info
                exit 0
            else
                echo -e "${YELLOW}Starting existing container...${NC}"
                docker start "${CONTAINER_NAME}"
                show_connection_info
                exit 0
            fi
        fi
    fi
}

# Function to pull the latest image
pull_image() {
    echo -e "${YELLOW}Pulling the latest Cosmos DB emulator image...${NC}"
    docker pull "${IMAGE_NAME}"
    echo -e "${GREEN}✅ Image pulled successfully${NC}"
}

# Function to start the emulator
start_emulator() {
    echo -e "${YELLOW}Starting Azure Cosmos DB vNext Emulator...${NC}"
    echo -e "${BLUE}Configuration:${NC}"
    echo -e "  - Container Name: ${CONTAINER_NAME}"
    echo -e "  - Image: ${IMAGE_NAME}"
    echo -e "  - Protocol: ${PROTOCOL}"
    echo -e "  - Cosmos Port: ${COSMOS_PORT}"
    echo -e "  - Explorer Port: ${EXPLORER_PORT}"
    echo -e "  - Log Level: ${LOG_LEVEL}"
    echo ""

    # Start the container (without persistent storage to avoid permission issues on Windows)
    # Note: Data will be lost when container is removed
    docker run \
        --detach \
        --name "${CONTAINER_NAME}" \
        --publish "${COSMOS_PORT}:8081" \
        --publish "${EXPLORER_PORT}:1234" \
        "${IMAGE_NAME}" \
        --protocol "${PROTOCOL}" \
        --log-level "${LOG_LEVEL}" \
        --enable-telemetry false

    echo -e "${GREEN}✅ Cosmos DB emulator started successfully!${NC}"
}

# Function to wait for emulator to be ready
wait_for_emulator() {
    echo -e "${YELLOW}Waiting for emulator to be ready...${NC}"
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        # Check if container is running
        if ! docker ps --filter "name=${CONTAINER_NAME}" --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
            echo -e "${RED}❌ Container stopped unexpectedly${NC}"
            docker logs "${CONTAINER_NAME}"
            exit 1
        fi

        # Try to connect to the emulator
        if curl -k -s -f "https://localhost:${COSMOS_PORT}/_explorer/emulator.pem" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Emulator is ready!${NC}"
            return 0
        fi

        echo -n "."
        sleep 2
        ((attempt++))
    done

    echo -e "${RED}❌ Emulator failed to start within expected time${NC}"
    echo -e "${YELLOW}Container logs:${NC}"
    docker logs "${CONTAINER_NAME}"
    exit 1
}

# Function to show connection information
show_connection_info() {
    echo ""
    echo -e "${GREEN}=== Connection Information ===${NC}"
    echo -e "${BLUE}Cosmos DB Endpoint:${NC} https://localhost:${COSMOS_PORT}/"
    echo -e "${BLUE}Data Explorer:${NC} http://localhost:${EXPLORER_PORT}/"
    echo ""
    echo -e "${GREEN}=== Default Connection Details ===${NC}"
    echo -e "${BLUE}AccountEndpoint:${NC} https://localhost:${COSMOS_PORT}/"
    echo -e "${BLUE}AccountKey:${NC} C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
    echo ""
    echo -e "${GREEN}=== Connection String ===${NC}"
    echo "AccountEndpoint=https://localhost:${COSMOS_PORT}/;AccountKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==;"
    echo ""
    echo -e "${YELLOW}=== Important Notes ===${NC}"
    echo "• This is the vNext preview version with limited features"
    echo "• Only NoSQL API is supported"
    echo "• For .NET/Java apps, HTTPS is enabled by default"
    echo "• Data is NOT persistent (lost when container is removed)"
    echo "• Certificate available at: https://localhost:${COSMOS_PORT}/_explorer/emulator.pem"
    echo ""
    echo -e "${GREEN}=== Management Commands ===${NC}"
    echo -e "${BLUE}View logs:${NC} docker logs ${CONTAINER_NAME}"
    echo -e "${BLUE}Stop emulator:${NC} docker stop ${CONTAINER_NAME}"
    echo -e "${BLUE}Remove emulator:${NC} docker rm -f ${CONTAINER_NAME}"
    echo -e "${BLUE}Container status:${NC} docker ps -a --filter name=${CONTAINER_NAME}"
}

# Function to download certificate (for Java SDK)
download_certificate() {
    echo -e "${YELLOW}Downloading emulator certificate...${NC}"
    curl -k -s "https://localhost:${COSMOS_PORT}/_explorer/emulator.pem" > cosmos_emulator.crt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Certificate downloaded as 'cosmos_emulator.crt'${NC}"
        echo -e "${BLUE}For Java SDK, import with:${NC}"
        echo "keytool -cacerts -importcert -alias cosmos_emulator -file cosmos_emulator.crt -storepass changeit -noprompt"
    else
        echo -e "${RED}❌ Failed to download certificate${NC}"
    fi
}

# Main execution
main() {
    check_docker
    check_existing_container
    pull_image
    start_emulator
    wait_for_emulator
    show_connection_info
    
    # Optionally download certificate
    read -p "Download SSL certificate for Java SDK? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        download_certificate
    fi
    
    echo -e "${GREEN}🚀 Azure Cosmos DB vNext Emulator is ready for development!${NC}"
}

# Handle command line arguments
case "${1:-}" in
    "stop")
        echo -e "${YELLOW}Stopping Cosmos DB emulator...${NC}"
        docker stop "${CONTAINER_NAME}" || true
        echo -e "${GREEN}✅ Emulator stopped${NC}"
        ;;
    "remove")
        echo -e "${YELLOW}Removing Cosmos DB emulator container...${NC}"
        docker rm -f "${CONTAINER_NAME}" || true
        echo -e "${GREEN}✅ Container removed${NC}"
        ;;
    "logs")
        docker logs "${CONTAINER_NAME}"
        ;;
    "status")
        docker ps -a --filter "name=${CONTAINER_NAME}"
        ;;
    "cert")
        download_certificate
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)  Start the emulator"
        echo "  stop       Stop the emulator"
        echo "  remove     Remove the emulator container"
        echo "  logs       Show emulator logs"
        echo "  status     Show container status"
        echo "  cert       Download SSL certificate"
        echo "  help       Show this help"
        ;;
    "")
        main
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
