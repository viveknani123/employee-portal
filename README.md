# Employee Productivity & Digital Wellbeing Monitoring System

A Django-based web application for tracking employee productivity and digital wellbeing, containerized with Docker, backed by PostgreSQL, and deployed on Kubernetes (k3s) on AWS EC2 with a full CI/CD pipeline.

## Features

- User registration and authentication
- Productivity tracking dashboard
- PostgreSQL database backend
- Fully containerized with Docker & Docker Compose
- Deployed on Kubernetes (k3s) with multi-replica app + separate DB service
- Automated CI/CD pipeline (GitHub Actions): build → test → push to Docker Hub → auto-deploy to Kubernetes on every push to main

## Tech Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (k3s)
- **Infrastructure as Code:** Terraform (AWS EC2, Security Groups)
- **CI/CD:** GitHub Actions
- **Cloud:** AWS (EC2, EBS gp3)
- **Frontend:** HTML, CSS

## Architecture

GitHub Push (main)
|
GitHub Actions CI/CD
|-- Run Django checks
|-- Build Docker image
|-- Push to Docker Hub
|-- SSH to EC2 --> kubectl rollout restart
|
AWS EC2 (Terraform-provisioned)
|
k3s (Kubernetes)
|-- Deployment: employee-portal (2 replicas, NodePort 30080)
|-- Deployment: db (PostgreSQL, ClusterIP service "db")


## Getting Started

### Run locally with Docker

```bash
git clone https://github.com/viveknani123/employee-portal.git
cd employee-portal
docker-compose up --build
```

App available at `http://localhost:8000`

### Run without Docker

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Kubernetes Deployment (Production-style)

Infrastructure is provisioned via Terraform (`terraform-aws-infra` repo), then deployed to a k3s cluster on EC2:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f postgres.yaml
```

Key engineering decisions:
- Upgraded EBS volume from gp2 to gp3 to resolve an I/O bottleneck (100 → 3000 baseline IOPS) that was causing API server timeouts under load on a t3.micro instance
- Added swap space to handle memory pressure on the 1GB RAM instance
- Used Kubernetes DNS-based service discovery (`db` service name) so the Django app connects to PostgreSQL without hardcoded IPs

## CI/CD Pipeline

On every push to `main`:
1. Run Django checks (`manage.py check`)
2. Build Docker image and push to Docker Hub
3. SSH into EC2 and trigger a rolling restart on the Kubernetes deployment

See `.github/workflows/` for the full pipeline definition.

## Project Structure

employee_portal/ - Django project settings
wellbeing/ - Core app (productivity tracking)
templates/ - HTML templates
static/ - Static assets (CSS/JS)
Dockerfile
docker-compose.yml
requirements.txt


## Future Enhancements

- Prometheus + Grafana monitoring (deprioritized due to RAM constraints on t3.micro; would need a larger instance or resource-tuned Helm charts)
- HTTPS via Ingress + cert-manager
- Multi-environment (dev/staging/prod) setup using Terraform workspaces

## Health Checks & Self-Healing
- Added `/health/` endpoint to the Django app for Kubernetes probes.
- Configured `readinessProbe` and `livenessProbe` in the Deployment spec — 
  Kubernetes now automatically restarts unresponsive pods and withholds 
  traffic from pods that aren't ready, improving reliability without manual intervention.

## Autoscaling & Metrics
- Installed `metrics-server` (with `--kubelet-insecure-tls`, required for self-managed k3s
  with self-signed kubelet certs) to enable `kubectl top` and CPU-based autoscaling.
- Added `resources.requests`/`limits` to the Deployment spec — required prerequisite for HPA,
  since percentage-based CPU targets need a baseline request value to compute against.
- Configured a HorizontalPodAutoscaler (`hpa.yaml`): min 2 / max 5 replicas, targeting 20% CPU
  utilization (intentionally low threshold for demo purposes on a low-traffic instance).
- Verified end-to-end: HPA correctly reads live CPU metrics (`kubectl get hpa` showed real
  percentages, not `<unknown>`). Ran a synthetic load test with parallel `busybox` pods hitting
  `/health/`; CPU peaked at ~12%, under the 20% threshold, so no scale-up event was observed.
  This confirmed the HPA pipeline (metrics-server → HPA → Deployment) is correctly wired,
  even though the specific test didn't generate enough load to cross the threshold.
