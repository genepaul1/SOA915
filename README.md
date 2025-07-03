# SOA915 - Microservices Monitoring with Prometheus & Grafana

This project demonstrates a microservices architecture with **Prometheus** and **Grafana** monitoring in Kubernetes using **Minikube**. It includes the following services:

- `user-service` (substitute for patient service)
- `appointment-service`
- `billing-service`
- `notification-service`

---

## 🚀 Prerequisites

- Docker
- Minikube
- kubectl
- Helm

---

## 📁 Project Structure

SOA915/
│
├── user_service/
│ └── main.py
│
├── appointment_service/
│ └── main.py
│
├── billing_service/
│ └── main.py
│
├── notification_service/
│ └── main.py
│
├── k8s/
│ ├── user-deployment.yaml
│ ├── appointment-deployment.yaml
│ ├── billing-deployment.yaml
│ ├── notification-deployment.yaml
│ ├── user-service-monitor.yaml
│ ├── ...
│
└── README.md


---

## ⚙️ Setup Instructions

### 1. Start Minikube

```bash
minikube start --driver=docker
```

2. Install Prometheus Operator via Helm
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
````
3. Build Docker Images
```bash
docker build -t user-service:latest ./user_service
docker build -t appointment-service:latest ./appointment_service
docker build -t billing-service:latest ./billing_service
docker build -t notification-service:latest ./notification_service
```
4. Apply Kubernetes Manifests
```bash
kubectl apply -f k8s/
```
5. Access Prometheus & Grafana
```bash
kubectl port-forward svc/prometheus-operated -n monitoring 9090:80
kubectl port-forward svc/grafana -n monitoring 3000:80
```

    Prometheus: http://localhost:9090

    Grafana: http://localhost:3000

        Username: admin

        Password: soa915

6. Check Services

Test locally:
```bash
kubectl port-forward svc/user-service 8000:8000
curl http://localhost:8000/metrics
```
Repeat for other services on their ports:
8001 (appointment), 8002 (billing), 8003 (notification)

📊 Dashboards

In Grafana:

    Add Prometheus as a data source (http://prometheus-operated.monitoring.svc:9090)

    Import dashboards (or create your own)

    Visualize metrics like request counters from each service

✅ Status

Prometheus monitors all 4 services

Grafana is running and visualizing metrics

All services expose /metrics and increment Prometheus counters
