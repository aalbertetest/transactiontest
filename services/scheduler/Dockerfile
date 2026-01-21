FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /bin/scheduler ./cmd/scheduler

FROM gcr.io/distroless/static:nonroot
COPY --from=build /bin/scheduler /bin/scheduler
USER 65532:65532
ENTRYPOINT ["/bin/scheduler"]
