Infrastructure
==============

Dockerfiles
-----------

Dockerfiles are provided per service in infra/docker/*.Dockerfile. Each image
is based on the Python runtime (standard library only) and uses the SERVICE_ONLY
environment variable to run a single service inside the shared runtime.

Example: infra/docker/api-gateway.Dockerfile

FROM python:3.11-slim
WORKDIR /app
COPY src/python/platform.py /app/platform.py
ENV SERVICE_ONLY=gateway
ENV GATEWAY_PORT=8080
EXPOSE 8080
CMD ["python", "/app/platform.py"]

To produce Go or TypeScript runtime images, replace the CMD with the Go binary
or Node process and copy the respective source/build output. The service
selection remains the same via SERVICE_ONLY.

Kubernetes Manifests
--------------------

The full multi-service manifest is in infra/k8s/platform.yaml. It includes:

* Namespace: platform
* ConfigMap: platform-config
* Secret: platform-secrets
* Deployments and Services for all core services

Each deployment uses readiness/liveness probes and centralized configuration.

Helm Charts
-----------

Helm chart is located in infra/helm with:

* Chart.yaml and values.yaml
* templates/namespace.yaml
* templates/configmap.yaml
* templates/secret.yaml
* templates/deployments.yaml
* templates/services.yaml

Values define the service list and port mappings and allow easy overrides.

Terraform Examples
------------------

infra/terraform/main.tf demonstrates:

* Kubernetes provider configuration
* Helm provider configuration
* Namespace creation
* Helm release for the platform chart

CI/CD Pipeline
-------------

.github/workflows/ci.yml provides a pipeline that:

* Checks out code
* Runs Python syntax checks
* Runs Go tests/build
* Performs a Node.js sanity check

In production, expand this pipeline to include:

* Container build and vulnerability scans
* Integration tests against ephemeral environments
* Canary deployments with progressive delivery (Argo Rollouts, Flagger)

Secrets Management
------------------

Production secrets should use:

* Vault or cloud KMS for encryption
* SealedSecrets or External Secrets Operator for Kubernetes
* Automated key rotation with dual-write support

The repository includes a Kubernetes Secret template in the K8s manifest and
Helm chart for local demos.
