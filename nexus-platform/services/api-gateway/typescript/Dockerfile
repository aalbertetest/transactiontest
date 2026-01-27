# =============================================================================
# NEXUS PLATFORM - API GATEWAY - TYPESCRIPT DOCKERFILE
# =============================================================================
# Multi-stage build for production-ready Node.js API Gateway container.
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder
# -----------------------------------------------------------------------------
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build TypeScript
RUN npm run build

# Remove dev dependencies
RUN npm prune --production

# -----------------------------------------------------------------------------
# Stage 2: Production
# -----------------------------------------------------------------------------
FROM node:20-alpine AS production

# Labels
LABEL maintainer="Nexus Platform Team"
LABEL version="1.0.0"
LABEL description="Nexus Platform API Gateway (TypeScript)"

# Install runtime dependencies
RUN apk add --no-cache curl tini

# Create non-root user
RUN addgroup -g 1000 nexus && \
    adduser -u 1000 -G nexus -s /bin/sh -D nexus

# Set working directory
WORKDIR /app

# Copy production files
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Change ownership
RUN chown -R nexus:nexus /app

# Switch to non-root user
USER nexus

# Environment variables
ENV NODE_ENV=production \
    NODE_OPTIONS="--max-old-space-size=512"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Use tini as init system
ENTRYPOINT ["/sbin/tini", "--"]

# Run the application
CMD ["node", "dist/index.js"]

# -----------------------------------------------------------------------------
# Stage 3: Development
# -----------------------------------------------------------------------------
FROM node:20-alpine AS development

# Install development tools
RUN apk add --no-cache curl git

# Create non-root user
RUN addgroup -g 1000 nexus && \
    adduser -u 1000 -G nexus -s /bin/sh -D nexus

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies
RUN npm install

# Change ownership
RUN chown -R nexus:nexus /app

# Switch to non-root user
USER nexus

# Environment variables
ENV NODE_ENV=development

# Expose port
EXPOSE 8080

# Run with hot reload
CMD ["npm", "run", "dev"]
