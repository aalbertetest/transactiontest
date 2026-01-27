# =============================================================================
# NEXUS PLATFORM - API GATEWAY - GO DOCKERFILE
# =============================================================================
# Multi-stage build for production-ready Go API Gateway container.
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder
# -----------------------------------------------------------------------------
FROM golang:1.21-alpine AS builder

# Install build dependencies
RUN apk add --no-cache git ca-certificates tzdata

# Set working directory
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build arguments
ARG VERSION=1.0.0
ARG BUILD_TIME
ARG GIT_COMMIT

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-w -s -X main.Version=${VERSION} -X main.BuildTime=${BUILD_TIME} -X main.GitCommit=${GIT_COMMIT}" \
    -o /app/api-gateway \
    ./cmd/server

# -----------------------------------------------------------------------------
# Stage 2: Production
# -----------------------------------------------------------------------------
FROM alpine:3.19 AS production

# Labels
LABEL maintainer="Nexus Platform Team"
LABEL version="1.0.0"
LABEL description="Nexus Platform API Gateway (Go)"

# Install runtime dependencies
RUN apk add --no-cache ca-certificates tzdata curl

# Create non-root user
RUN addgroup -g 1000 nexus && \
    adduser -u 1000 -G nexus -s /bin/sh -D nexus

# Set working directory
WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/api-gateway /app/api-gateway

# Copy timezone data
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo

# Create directories
RUN mkdir -p /var/log/nexus && \
    chown -R nexus:nexus /var/log/nexus /app

# Switch to non-root user
USER nexus

# Environment variables
ENV TZ=UTC

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the binary
ENTRYPOINT ["/app/api-gateway"]

# -----------------------------------------------------------------------------
# Stage 3: Development
# -----------------------------------------------------------------------------
FROM golang:1.21-alpine AS development

# Install development tools
RUN apk add --no-cache git ca-certificates tzdata curl

# Install air for hot reload
RUN go install github.com/cosmtrek/air@latest

# Set working directory
WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Create non-root user
RUN addgroup -g 1000 nexus && \
    adduser -u 1000 -G nexus -s /bin/sh -D nexus

# Change ownership
RUN chown -R nexus:nexus /app /go

# Switch to non-root user
USER nexus

# Expose port
EXPOSE 8080

# Run with hot reload
CMD ["air", "-c", ".air.toml"]
