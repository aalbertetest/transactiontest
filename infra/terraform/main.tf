terraform {
  required_version = ">= 1.5.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.25.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.12.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}

resource "kubernetes_namespace" "platform" {
  metadata {
    name = "platform"
  }
}

resource "helm_release" "platform" {
  name       = "platform"
  chart      = "${path.module}/../helm"
  namespace  = kubernetes_namespace.platform.metadata[0].name
  depends_on = [kubernetes_namespace.platform]
  values     = [file("${path.module}/../helm/values.yaml")]
}
