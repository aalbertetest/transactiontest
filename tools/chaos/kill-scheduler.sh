#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-workflow-engine}"

pod=$(kubectl get pods -n "$NAMESPACE" -l app=dwe-scheduler -o name | head -n 1)
echo "Deleting $pod"
kubectl delete -n "$NAMESPACE" "$pod"
