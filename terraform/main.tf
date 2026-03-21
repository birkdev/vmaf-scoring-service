terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.24.0"
    }
  }
}


provider "google" {
  project = "vmaf-scoring-service"
  region  = "europe-north1"
}


resource "google_cloud_run_v2_service" "default" {
  name                = "vmaf-scoring-service"
  location            = "europe-north1"
  deletion_protection = false

  template {
    scaling {
      max_instance_count = 1
    }
    containers {
      name = "vmaf-scoring-service"
      ports {
        container_port = 8000
      }
      image = "gcr.io/vmaf-scoring-service/vmaf-scoring-service"
      resources {
        limits = {
          memory = "2Gi"
        }
      }
    }
  }
}


resource "google_cloud_run_v2_service_iam_member" "public" {
  name     = google_cloud_run_v2_service.default.name
  location = google_cloud_run_v2_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}