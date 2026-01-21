#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-workflow-engine}"
COUNT="${COUNT:-1}"

pods=$(kubectl get pods -n "$NAMESPACE" -l app=dwe-executor -o name | head -n "$COUNT")
for pod in $pods; do
  echo "Deleting $pod"
  kubectl delete -n "$NAMESPACE" "$pod"
done
