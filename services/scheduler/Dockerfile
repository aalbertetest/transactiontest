# Build Stage
FROM golang:1.24-alpine AS builder

WORKDIR /app

# Copy shared lib
COPY lib/go /lib/go

# Copy service
COPY services/scheduler /services/scheduler
WORKDIR /services/scheduler

# Fix go.mod to point to local lib
RUN go mod edit -replace github.com/cursor/platform/lib/go=/lib/go
RUN go mod download

RUN CGO_ENABLED=0 GOOS=linux go build -o /scheduler ./cmd/server

# Final Stage
FROM alpine:3.19

WORKDIR /app
COPY --from=builder /scheduler .

CMD ["./scheduler"]
