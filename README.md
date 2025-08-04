# SOA915 - Microservices Monitoring with Prometheus & Grafana

This repository contains a microservices architecture project built with Python (Flask/FastAPI), Docker, and Kubernetes (Minikube). It demonstrates service orchestration, monitoring with Prometheus and Grafana, and CI/CD integration using GitHub Actions.

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
- Prometheus & Grafana – Monitoring and visualization
- GitHub Actions – CI pipeline for unit tests
- Unit tests with `pytest`
- Inter-service communication via REST APIs


## 📁 Project Structure
```

SOA915/
│
├── .github/workflows/ 
│ └── ci-unit-tests.yml
│
├── appointment_service/
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt
│ ├── appointments.db
│ ├── tests/
│ │ └── unit/
│ │ └── test_appointment_unit.py
│ │ └── integration/
│ │ └── test_appointment_service.py
│
├── billing_service/
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt
│ ├── tests/
│ │ └── unit/
│ │ └── test_billing_service.py
│ │ └── integration/
│ │ └── test_billing_service.py
│
├── user_service/
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt
│ ├── tests/
│ │ └── unit/
│ │ └── test_user_unit.py
│ │ └── integration/
│ │ └── test_user_service.py
│
├── notification_service/
│ ├── Dockerfile
│ ├── main.py
│ ├── requirements.txt
│ ├── tests/
│ │ └── unit/
│ │ └── test_notification_unit.py
│ │ └── integration/
│ │ └── test_notification_service.py\
│
├── k8s/
│   ├── user-deployment.yaml
│   ├── appointment-deployment.yaml
│   ├── user-service-monitor.yaml
│   ├── appointment-service-monitor.yaml
│   ├── appointment-service.yaml
│   ├── billing-deployment.yaml
│   ├── billing-service-monitor.yaml
│   ├── billing-service.yaml
│   ├── user-service.yaml
│   ├── notification-service-monitor.yaml
│   ├── notification-deployment.yaml
│   └── hpa.yaml
│
├── frontend/
│ └── index.html
│ 
├── README.md

```

## ⚙️ Setup Instructions

### Start Minikube

```bash
minikube start --driver=docker
```

Add Prometheus Operator and Grafana via Helm
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
````

Install Prometheus and Grafana
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

Apply Kubernetes Manifests
```bash
kubectl apply -f k8s/
```

Access Prometheus & Grafana
```bash
kubectl port-forward svc/prometheus-server -n monitoring 9090:80
kubectl port-forward svc/grafana -n monitoring 3000:80
```

    Prometheus: http://localhost:9090

    Grafana: http://localhost:3000

        Username: admin

        Password: soa915

## 🧪 Local Unit Testing

Each microservice has a `tests/unit` folder with basic tests using `pytest`.

### ✅ How to Run Tests Locally

1. Navigate to the specific microservice folder:

```bash
cd appointment_service  # or user_service, billing_service, notification_service
```

Repeat for other services on their ports:
```bash
8000 (user), 8001 (appointment), 8002 (billing), 8003 (notification)
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install pytest

```

4. Run tests:
```bash
pytest tests/unit

```


Booking Interactions (manually using curl and specific microservice port):
```bash
kubectl port-forward svc/appointment-service 8001:8001
curl -X POST http://localhost:8001/book -H "Content-Type: application/json" -d '{"name": "John"}'
```

This call:

    Increments the appointment counter
    
    Triggers both billing and notification services
    

    
### Sample CI Step (from `.github/workflows/ci-unit-tests.yml`)
In the repository, run this yaml file to automatically test the 4 microservices
```yaml
- name: Run unit tests for ${{ matrix.service }}
   working-directory: ${{ matrix.service }}
   run: |
   python -m venv venv
  ./venv/bin/pip install --upgrade pip
  ./venv/bin/pip install -r requirements.txt
  ./venv/bin/pip install pytest
  ./venv/bin/python -m pytest tests/unit

```


🌐 Frontend Usage

The frontend is a simple HTML page (index.html) that interacts with the microservices we've created in the backend.
How to Use

1. Start all microservices locally.

2. Go to frontend folder
  
3. Open index.html in your browser (double-click or use a local web server):
   
``` bash
# Optional: use a simple Python server
python3 -m http.server 8080

```

4. Fill out the appointment form and click Submit.

  This will send a POST request to the /book endpoint.
  
  On success, it triggers downstream requests to billing_service and notification_service.

5. Fill out user registration form and click Submit

  This will send a POST request to the /register endpoint.
  
  On success, it triggers downstream requests to user_service.

4. Confirm results in:

  The UI (success or error message).

  Or on our terminal logs or Prometheus metrics.

  

📊 Dashboards

In Grafana:

    Add Prometheus as a data source (http://prometheus-operated.monitoring.svc:9090)

All microservices expose Prometheus-compatible metrics on /metrics

Dashboards are configured in Grafana for:

    Request volume

    Response time

    Error rate

    Service health

Horizontal Pod Autoscalers (HPAs) are deployed per microservice:

    Automatically scale replicas based on CPU usage

    Ensures services remain responsive under load

    

🧰 Microservices Endpoints Summary

| Service               | Local Port | NodePort | Health Check | Metrics    |
| --------------------- | ---------- | -------- | ------------ | ---------- |
| appointment\_service  | `8001`     | `30002`  | `/health`    | `/metrics` |
| billing\_service      | `8002`     | `31837`  | `/health`    | `/metrics` |
| notification\_service | `8003`     | `30628`  | `/health`    | `/metrics` |
| user\_service         | `8000`     | `32680`  | `/health`    | `/metrics` |



Troubleshooting

If you encounter issues, check the logs:
``` bash
  kubectl logs <pod-name>
``` 
  Or describe the deployment:
``` bash
  kubectl describe deployment <deployment-name>
```

---
Contributing:

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions or improvements.


---

Team Members:

Gene Paul Dizon

Jae Hun Yang

Ashika Sapkota

Meet Sandipkumar Thakkar


