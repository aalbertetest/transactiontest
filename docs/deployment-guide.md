Deployment Guide
================

Local Docker Deployment
-----------------------

Build a service image:

  docker build -f infra/docker/api-gateway.Dockerfile -t platform/api-gateway:latest .

Run locally:

  docker run -p 8080:8080 -e JWT_SECRET=dev-secret platform/api-gateway:latest

Repeat for each service as needed.

Kubernetes Deployment
---------------------

Apply the manifest:

  kubectl apply -f infra/k8s/platform.yaml

Validate:

  kubectl -n platform get pods
  kubectl -n platform get svc

Helm Deployment
---------------

Install:

  helm install platform infra/helm -n platform --create-namespace

Upgrade:

  helm upgrade platform infra/helm -n platform

Terraform Deployment
--------------------

Initialize and apply:

  terraform -chdir=infra/terraform init
  terraform -chdir=infra/terraform apply

Rollback Strategy
-----------------

* Use rolling updates with maxUnavailable=0.
* Canary deployments for gateway and auth.
* Maintain versioned Helm releases for easy rollback.
