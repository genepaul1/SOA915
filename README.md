# SOA915 - Microservices Monitoring with Prometheus & Grafana

This project demonstrates a microservices architecture using Kubernetes, FastAPI, Flask, Prometheus, and Grafana. It consists of four core microservices deployed on a local Kubernetes cluster using Minikube.

## 📦 Microservices

| Service Name           | Framework | Description                                   | Exposes Metrics |
|------------------------|-----------|-----------------------------------------------|-----------------|
| `user-service`         | FastAPI   | Handles user registration                     | ✅              |
| `appointment-service`  | Flask     | Books appointments and triggers other services| ✅              |
| `billing-service`      | FastAPI   | Simulates billing requests                    | ✅              |
| `notification-service` | FastAPI   | Simulates user notifications                  | ✅              |

### 🔄 Service Interactions

- `appointment-service` calls:
  - `billing-service` to simulate charging the user
  - `notification-service` to simulate sending a notification

---

## 🚀 Prerequisites

- [Minikube](https://minikube.sigs.k8s.io/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/)
- Docker installed and configured



## 📁 Project Structure
```

soa915/
├── appointment_service/
│   └── main.py
├── billing_service/
│   └── main.py
├── notification_service/
│   └── main.py
├── user_service/
│   └── main.py
├── k8s/
│   ├── user-deployment.yaml
│   ├── appointment-deployment.yaml
│   ├── billing-deployment.yaml
│   ├── notification-deployment.yaml
│   ├── *.service.yaml
│   └── *.service-monitor.yaml
└── README.md

```

## ⚙️ Setup Instructions

### 1. Start Minikube

```bash
minikube start --driver=docker
```

2. Add Prometheus Operator and Grafana via Helm
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
````

3. Install Prometheus and Grafana
```bash
helm install prometheus prometheus-community/prometheus --namespace monitoring --create-namespace
helm install grafana grafana/grafana --namespace monitoring
```

4. Build Docker Images
```bash
eval $(minikube docker-env)
docker build -t user-service:latest ./user_service
docker build -t appointment-service:latest ./appointment_service
docker build -t billing-service:latest ./billing_service
docker build -t notification-service:latest ./notification_service
```
5. Apply Kubernetes Manifests
```bash
kubectl apply -f k8s/
```
6. Access Prometheus & Grafana
```bash
kubectl port-forward svc/prometheus-server -n monitoring 9090:80
kubectl port-forward svc/grafana -n monitoring 3000:80
```

    Prometheus: http://localhost:9090

    Grafana: http://localhost:3000

        Username: admin

        Password: soa915

7. Check Services

Test locally:
```bash
kubectl port-forward svc/user-service 8000:8000
curl http://localhost:8000/metrics
```
Repeat for other services on their ports:
8001 (appointment), 8002 (billing), 8003 (notification)

Booking Interactions:
```bash
kubectl port-forward svc/appointment-service 8001:8001
curl -X POST http://localhost:8001/book -H "Content-Type: application/json" -d '{"name": "John"}'
```
This call:

    Increments the appointment counter
    
    Triggers both billing and notification services
    
📊 Dashboards

In Grafana:

    Add Prometheus as a data source (http://prometheus-operated.monitoring.svc:9090)

    Import dashboards (or create your own)

    Visualize metrics like request counters from each service

✅ Status

Prometheus monitors all 4 services

Grafana is running and visualizing metrics

All services expose /metrics and increment Prometheus counters
