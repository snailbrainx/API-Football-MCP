#!/bin/bash
set -e

CONTAINER_NAME="api-football-mcp"
IMAGE_NAME="api-football-mcp"
PORT=8111

echo "=== API-Football MCP Server Deploy ==="

# Stop and remove existing container if running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping existing container..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
fi

# Build the image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME" .

# Run the container
echo "Starting container on port $PORT..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "${PORT}:${PORT}" \
    --env-file .env \
    --restart unless-stopped \
    "$IMAGE_NAME"

# Wait for startup
echo "Waiting for server to start..."
sleep 3

# Health check
echo "Testing server..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    http://localhost:${PORT}/mcp \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"deploy-test","version":"1.0"}}}')

if [ "$RESPONSE" = "200" ]; then
    echo "Server is running on port $PORT"
    echo "MCP endpoint: http://$(hostname -I | awk '{print $1}'):${PORT}/mcp"
    echo ""
    echo "Container logs:"
    docker logs "$CONTAINER_NAME" 2>&1 | tail -5
else
    echo "ERROR: Server returned HTTP $RESPONSE"
    echo "Container logs:"
    docker logs "$CONTAINER_NAME" 2>&1
    exit 1
fi
