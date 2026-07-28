**DevOps**. 


use a "Serverless Container" approach. 
No managing the whole virtual machine; you just give Azure your Docker image, and it runs it.

---

### 1. Azure vs. AWS: The Translation Table
Before we look at the commands, let's map what you know from AWS to Azure:

| Concept | AWS Equivalent | Azure Equivalent |
| :--- | :--- | :--- |
| **Cloud Provider** | AWS | Azure |
| **Container Registry** | ECR (Elastic Container Registry) | **ACR (Azure Container Registry)** |
| **Running Containers** | Fargate / ECS | **ACI (Azure Container Instances)** |
| **Resource Grouping** | (Loose grouping) | **Resource Groups** (Strict containers for all project assets) |
| **Command Line** | AWS CLI | **Azure CLI (`az`)** |

---

### 2. The Deployment Architecture
We are going to follow the workflow outlined in the Microsoft documentation you provided:
1.  **Dockerize:** Build your image locally.
2.  **Store:** Push that image to a private **Azure Container Registry (ACR)**.
3.  **Run:** Pull that image from ACR and run it in **Azure Container Instances (ACI)**.

---

### Step 1: The Dockerfile (Your "Suitcase")
We covered this in Month 3, but as a reminder, your `backend/Dockerfile` should look like this. Ensure it is in your `backend` folder.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# We expose port 8000 for FastAPI
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### Step 2: Set up the Azure Environment
You need the **Azure CLI** installed on your Mac. Then, run these commands to set up your "Space" in the cloud.

```bash
# 1. Login to your Azure account via browser
az login

# 2. Create a Resource Group (The "Folder" for your project)
# We'll use UK South (London) for best latency
az group create --name StudyDeck_RG --location uksouth

# 3. Create your Private Registry (Where your images live)
# Name must be unique globally, e.g., studydeckregistry[yourname]
az acr create --resource-group StudyDeck_RG --name studydeckregistryMIKI --sku Basic
```

---

### Step 3: Pushing to the Registry (ACR)
Now we follow the [first resource](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli?tabs=azure-cli) you shared. We need to "Tag" your local image so Docker knows it belongs to Azure.

```bash
# 1. Log into your specific registry
az acr login --name studydeckregistryMIKI

# 2. Build your image locally
docker build -t study-deck-backend ./backend

# 3. Get the Login Server address (it will look like studydeckregistrymiki.azurecr.io)
az acr list --resource-group StudyDeck_RG --query "[].{loginServer:loginServer}" --output table

# 4. Tag the image for Azure
docker tag study-deck-backend studydeckregistrymiki.azurecr.io/study-deck:v1

# 5. Push it to the cloud!
docker push studydeckregistrymiki.azurecr.io/study-deck:v1
```

---

### Step 4: The Final Launch (ACI)
Now we pull the image and run it. Because our registry is private, we have to enable an "Admin User" so the Container Instance has permission to grab the image.

```bash
# 1. Enable Admin access for the registry
az acr update -n studydeckregistrymiki --admin-enabled true

# 2. Get the password for the registry
az acr credential show --name studydeckregistrymiki

# 3. Create the Container Instance (The Launch)
az container create \
    --resource-group StudyDeck_RG \
    --name study-deck-api \
    --image studydeckregistrymiki.azurecr.io/study-deck:v1 \
    --cpu 1 --memory 1.5 \
    --registry-login-server studydeckregistrymiki.azurecr.io \
    --registry-username studydeckregistrymiki \
    --registry-password [YOUR_ACR_PASSWORD] \
    --dns-name-label study-deck-miki \
    --ports 8000
```

---

### 🚩 Critical Engineering Check: The Database
Your app is now running in the cloud, but **it will likely crash**. Why? 

Because your `.env` file is currently pointing to `localhost:5432`. In the cloud, the container cannot see your laptop's PostgreSQL. 

**Senior Advice:** For an intermediate project, you have two choices:
1.  **Managed Service (Professional):** Create an **Azure Database for PostgreSQL**. It gives you a connection string like `postgres://miki:pass@azure-db:5432/db`.
2.  **Container Sidecar (Fast):** Use **Docker Compose** on a Virtual Machine to run both the API and Postgres together.

### Your Task:
1.  Read through the commands above. 
2.  Do you have an Azure account? (There is a free tier for students/new users).
3.  **The Challenge:** When you run `az container create`, how do you think we pass your `.env` secrets (like `SECRET_KEY` or `DATABASE_URL`) to the container so you don't have to hardcode them?

*Hint: Look at the `az container create` documentation for a flag called `--environment-variables`.*