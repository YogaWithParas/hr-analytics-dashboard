# 🚀 Deployment Guide - HR Analytics Dashboard

This guide covers all deployment options for the HR Analytics Dashboard, from local development to enterprise production environments.

## 📋 **Prerequisites**

- Python 3.8 or higher
- pip package manager
- Git (for version control)
- 4GB+ RAM (recommended for data processing)

## 🏠 **Local Development Deployment**

### **Step 1: Clone and Setup**
```bash
# Clone the repository
git clone https://github.com/yourusername/hr-analytics-dashboard.git
cd hr-analytics-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 2: Run Locally**
```bash
cd dashboard
streamlit run streamlit_app.py
```

### **Step 3: Access Dashboard**
- Open browser: `http://localhost:8501`
- Dashboard loads automatically with sample data

## ☁️ **Streamlit Cloud Deployment (Recommended for Demo)**

### **Step 1: Prepare Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### **Step 2: Deploy to Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `yourusername/hr-analytics-dashboard`
5. Set main file path: `dashboard/streamlit_app.py`
6. Click "Deploy!"

### **Step 3: Configure Environment**
- **Python version**: 3.8
- **Dependencies**: Automatically detected from `requirements.txt`
- **Environment variables**: Add if needed

### **Step 4: Access Live Demo**
- Your dashboard will be available at: `https://your-app-name.streamlit.app`
- Perfect for client demos and presentations

## 🐳 **Docker Deployment**

### **Step 1: Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the application
CMD ["streamlit", "run", "dashboard/streamlit_app.py"]
```

### **Step 2: Build and Run**
```bash
# Build Docker image
docker build -t hr-analytics-dashboard .

# Run container
docker run -p 8501:8501 hr-analytics-dashboard

# Access at: http://localhost:8501
```

### **Step 3: Docker Compose (Optional)**
```yaml
# docker-compose.yml
version: '3.8'
services:
  hr-dashboard:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## ☁️ **Cloud Platform Deployment**

### **AWS Deployment**

#### **Option 1: AWS App Runner**
```bash
# Install AWS CLI and configure
aws configure

# Deploy using App Runner
aws apprunner create-service \
    --service-name hr-analytics-dashboard \
    --source-configuration file://apprunner-source-config.json
```

#### **Option 2: AWS ECS with Fargate**
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name hr-dashboard-cluster

# Deploy service
aws ecs create-service \
    --cluster hr-dashboard-cluster \
    --service-name hr-dashboard-service \
    --task-definition hr-dashboard-task
```

### **Google Cloud Platform**

#### **Option 1: Cloud Run**
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/hr-dashboard

# Deploy to Cloud Run
gcloud run deploy hr-dashboard \
    --image gcr.io/PROJECT_ID/hr-dashboard \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

#### **Option 2: App Engine**
```yaml
# app.yaml
runtime: python39
entrypoint: streamlit run dashboard/streamlit_app.py

env_variables:
  STREAMLIT_SERVER_PORT: 8080
  STREAMLIT_SERVER_ADDRESS: 0.0.0.0
```

### **Microsoft Azure**

#### **Option 1: Azure Container Instances**
```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image hr-dashboard .

# Deploy to Container Instances
az container create \
    --resource-group myResourceGroup \
    --name hr-dashboard \
    --image myregistry.azurecr.io/hr-dashboard \
    --ports 8501
```

#### **Option 2: Azure App Service**
```bash
# Deploy to App Service
az webapp create \
    --resource-group myResourceGroup \
    --plan myAppServicePlan \
    --name hr-dashboard \
    --deployment-container-image-name myregistry.azurecr.io/hr-dashboard
```

## 🏢 **Enterprise Deployment**

### **On-Premises Deployment**

#### **Option 1: Kubernetes**
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hr-analytics-dashboard
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hr-dashboard
  template:
    metadata:
      labels:
        app: hr-dashboard
    spec:
      containers:
      - name: hr-dashboard
        image: hr-analytics-dashboard:latest
        ports:
        - containerPort: 8501
        env:
        - name: STREAMLIT_SERVER_PORT
          value: "8501"
---
apiVersion: v1
kind: Service
metadata:
  name: hr-dashboard-service
spec:
  selector:
    app: hr-dashboard
  ports:
  - port: 80
    targetPort: 8501
  type: LoadBalancer
```

#### **Option 2: Docker Swarm**
```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml hr-dashboard
```

### **Load Balancer Configuration**
```nginx
# nginx.conf
upstream hr_dashboard {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    listen 80;
    server_name hr-dashboard.yourcompany.com;

    location / {
        proxy_pass http://hr_dashboard;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 **Security Configuration**

### **Environment Variables**
```bash
# .env file
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

### **Authentication Setup**
```python
# Add to streamlit_app.py
import streamlit_authenticator as stauth

# Configure authentication
names = ['Admin', 'User1', 'User2']
usernames = ['admin', 'user1', 'user2']
passwords = ['admin123', 'user123', 'user456']

hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'hr_dashboard', 'auth_key', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')
```

## 📊 **Monitoring & Logging**

### **Health Check Endpoint**
```python
# Add to streamlit_app.py
import psutil
import time

def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "memory_usage": psutil.virtual_memory().percent,
        "cpu_usage": psutil.cpu_percent()
    }

# Display health metrics
if st.sidebar.checkbox("Show System Health"):
    health = health_check()
    st.sidebar.json(health)
```

### **Logging Configuration**
```python
# logging_config.py
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('hr_dashboard.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
```

## 🚀 **Performance Optimization**

### **Caching Configuration**
```python
# Add to streamlit_app.py
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    # Your data loading logic
    pass

@st.cache_resource
def create_charts():
    # Your chart creation logic
    pass
```

### **Memory Management**
```python
# Add memory monitoring
import psutil
import gc

def monitor_memory():
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        gc.collect()
        st.warning("High memory usage detected. Garbage collection performed.")
```

## 📱 **Mobile Optimization**

### **Responsive Design**
```python
# Add to streamlit_app.py
st.markdown("""
<style>
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            flex-direction: column;
        }
        .stMetric {
            font-size: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)
```

## 🔄 **CI/CD Pipeline**

### **GitHub Actions**
```yaml
# .github/workflows/deploy.yml
name: Deploy HR Dashboard

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Deploy to Streamlit Cloud
      run: |
        # Add your deployment logic here
        echo "Deployment completed"
```

## 📞 **Support & Troubleshooting**

### **Common Issues**

#### **Port Already in Use**
```bash
# Find process using port 8501
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # macOS/Linux

# Kill process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # macOS/Linux
```

#### **Memory Issues**
```bash
# Increase memory limit for Streamlit
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
export STREAMLIT_SERVER_MAX_MESSAGE_SIZE=200
```

#### **Dependency Conflicts**
```bash
# Clean install
pip uninstall -r requirements.txt -y
pip cache purge
pip install -r requirements.txt
```

### **Performance Monitoring**
```python
# Add performance monitoring
import time

def measure_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        st.sidebar.metric(f"{func.__name__} Time", f"{(end_time - start_time):.2f}s")
        return result
    return wrapper
```

## 🎯 **Demo Preparation Checklist**

- [ ] **Local Testing**: Ensure dashboard runs without errors
- [ ] **Data Validation**: Verify sample data loads correctly
- [ ] **Performance Check**: Test with large datasets
- [ ] **Mobile Testing**: Verify responsive design
- [ ] **Documentation**: Update README and deployment guides
- [ ] **Screenshots**: Capture dashboard screenshots for documentation
- [ ] **Demo Script**: Prepare presentation script
- [ ] **Backup Plan**: Have local version ready as backup

---

**🚀 Your HR Analytics Dashboard is now ready for professional deployment and client demos!**

For additional support, refer to the [Streamlit documentation](https://docs.streamlit.io/) or create an issue in the repository. 