# 🛡️ Kubernetes Deployment Report for Flask API Blog [DockerHub](https://hub.docker.com/r/onyxwizard/flask-api-blog)

A full breakdown of how the Flask API blog was deployed on **Kubernetes** using Minikube.

## 1. 🧰 Prerequisites & Setup

Before deploying your Flask app to Kubernetes, ensure these tools are installed:

| Tool | Version | Why |
|------|--------|-----|
| **Minikube** | v1.35+ | To run a local Kubernetes cluster |
| **kubectl** | v1.27+ | To interact with your Kubernetes cluster |
| **Docker Desktop** | Latest | For containerization and Minikube Docker context |
| **Git Bash / PowerShell** | - | To run terminal commands on Windows |

### 🐳 Optional: Install Helm (for advanced deployments)

```bash
choco install kubernetes-helm
```



## 2. 📦 Containerizing the Flask App

Your Flask API blog is already containerized in Docker using a `Dockerfile`:

### 📄 Dockerfile Recap

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

You built it with:

```bash
docker build -t flask-api-blog:latest .
```

Then tagged and pushed to Docker Hub:

```bash
docker tag flask-api-blog:latest onyxwizard/flask-api-blog:latest
docker push onyxwizard/flask-api-blog:latest
```

Or loaded into Minikube:

```bash
minikube image load flask-api-blog:latest
```


## 3. ☸️ Understanding Kubernetes Concepts

Let’s break down what **Kubernetes** is doing under the hood.

### 🧱 Core Concepts

#### 🎯 Pod
- The smallest deployable unit in Kubernetes.
- A pod runs one or more containers (e.g., your Flask app).
- Your deployment created two pods:
  ```bash
  NAME                             READY   STATUS    RESTARTS   AGE
  flask-cyber-kb-857b56cbbc-5w7lv   1/1     Running   0          119s
  flask-cyber-kb-857b56cbbc-zw4qq   1/1     Running   0          119s
  ```

#### 🏗️ Deployment
- Manages replicas of your pods.
- Ensures your app is always running.
- Defined in `k8s/deployment.yaml`.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-cyber-kb
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-cyber-kb
  template:
    metadata:
      labels:
        app: flask-cyber-kb
    spec:
      containers:
        - name: flask-cyber-kb
          image: flask-api-blog:latest
          ports:
            - containerPort: 5000
```

> ✅ You’re now running 2 replicas of your Flask app inside Kubernetes.



## 4. 🌐 Services: Exposing the App

### 🔹 What Is a Service?

Services define how to access your app inside the cluster.

You used a **NodePort** service to expose your app externally.

#### 📄 `k8s/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-cyber-kb
spec:
  type: NodePort
  selector:
    app: flask-cyber-kb
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
      nodePort: 30001
```

### ⚙️ What This Does

| Part | Purpose |
|------|---------|
| `selector` | Routes traffic to pods labeled `app: flask-cyber-kb` |
| `port: 80` | In-cluster communication |
| `targetPort: 5000` | Port Flask listens on inside container |
| `nodePort: 30001` | External port exposed on Minikube IP |

You applied it with:

```bash
kubectl apply -f k8s/service.yaml
```

And checked status with:

```bash
kubectl get services
```

Output:

```
NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
flask-cyber-kb   NodePort    10.101.206.112   <none>        80:30001/TCP   2m3s
```


## 5. 🟢 Checking Status of Deployment

After applying your YAML files, always check:

### 🧪 Pods

```bash
kubectl get pods
```

Expected output:

```
NAME                              READY   STATUS    RESTARTS   AGE
flask-cyber-kb-857b56cbbc-5w7lv   1/1     Running   0          119s
flask-cyber-kb-857b56cbbc-zw4qq   1/1     Running   0          119s
```

✅ Both pods are healthy.

### 📋 Describe Pod (Optional Debugging)

```bash
kubectl describe pod flask-cyber-kb-857b56cbbc-5w7lv
```

Check under **Events** for any errors like `ImagePullBackOff`, `CrashLoopBackOff`, or missing dependencies.



## 6. 🌐 Networking in Kubernetes

Now comes the fun part: **why can't you access your app via browser?**

### ❓ Why `kubectl port-forward` Works but `NodePort` Doesn’t

You ran:

```bash
kubectl port-forward pod/flask-cyber-kb-857b56cbbc-5w7lv 5000:5000
```

Visited:

👉 [http://localhost:5000](http://localhost:5000)  
✅ It worked!

But when visiting:

👉 [http://`<minkube-ip>`:30001](http://`<minkube-ip>`:30001)  
🚫 Timed out 😞

Here's why:



## 7. 🚧 Troubleshooting: Why NodePort Fails

### 🔍 Possible Causes

| Cause | Description |
|-------|-------------|
| 🔒 **Windows Firewall / Antivirus** | Blocks incoming traffic on high ports (like 30001) |
| 🐳 **Minikube Driver Issue** | Some drivers (especially Docker Desktop) have network issues |
| 📡 **Flask Binding to `127.0.0.1`** | Only accessible within container unless bound to `0.0.0.0` |
| 🔄 **NodePort Already Taken** | Another service might be using port `30001` |
| 🧠 **Minikube VM Network Limitation** | Sometimes doesn’t expose ports directly |



## 8. 🧪 Tunneling to Fix Access

To bypass NodePort issues, I used:

```bash
kubectl port-forward pod/flask-cyber-kb-857b56cbbc-5w7lv 5000:5000
```

This forwards traffic from your local machine (`localhost:5000`) → to the pod (`containerPort:5000`)

### ✅ Why It Works

Because:
- It bypasses NodePort entirely
- Uses Kubernetes' internal proxy
- Requires no external firewall changes

You can now safely test:
- `/api/login`
- `/api/entries`
- Web templates



## 9. 🌊 LoadBalancer – Better Way to Expose

If you're moving toward production or want better exposure, use `LoadBalancer` instead of `NodePort`.

### 📄 Updated `service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-cyber-kb
spec:
  type: LoadBalancer
  selector:
    app: flask-cyber-kb
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
```

Apply:

```bash
kubectl apply -f k8s/service.yaml
```

Then start the tunnel:

```bash
minikube tunnel
```

Now visit:

👉 http://localhost:80  
✅ Should work without timeout

### 🧠 Why `LoadBalancer` Works Better

| Feature | NodePort | LoadBalancer |
|--------|----------|--------------|
| Port range | 30000–32767 | Any port (via tunnel) |
| Accessibility | Limited to Minikube IP | Easier via localhost |
| Tunnel needed | No | Yes (`minikube tunnel`) |
| Use case | Development | Closer to Production |



## 10. 📚 Summary of Components

| Component | Role |
|----------|------|
| `deployment.yaml` | Runs your Flask app in multiple pods |
| `service.yaml` | Exposes the app inside/outside the cluster |
| `kubectl port-forward` | Best for testing locally |
| `NodePort` | Good for dev, but has firewall limits |
| `LoadBalancer + minikube tunnel` | Most reliable for local prod-like testing |



## 11. 🧩 Bonus: Why `host='0.0.0.0'` Matters

In your Flask app (`main.py`), make sure you're binding to all interfaces:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

If it's set to `host='127.0.0.1'` → only the container itself can reach it.



## 12. 🧪 Final Checklist Before Deploying

| Task | Command |
|------|--------|
| ✅ Build Docker image | `docker build -t flask-api-blog:latest .` |
| ✅ Load into Minikube | `minikube image load flask-api-blog:latest` |
| ✅ Set correct imagePullPolicy | `imagePullPolicy: Never` if local |
| ✅ Label pods correctly | `app: flask-cyber-kb` |
| ✅ Use `0.0.0.0` in Flask | So it binds outside the container |
| ✅ Test with `port-forward` | Confirm Flask works inside pod |
| ✅ Try `LoadBalancer + minikube tunnel` | For browser access |
| ✅ Check logs for errors | `kubectl logs <pod-name>` |



## 🚀 Final Thoughts

You've successfully:

✅ Built a Docker image of your Flask app  
✅ Deployed it in Kubernetes  
✅ Used `kubectl port-forward` to verify functionality  
✅ Switched from `NodePort` to `LoadBalancer`  
✅ Learned about core K8s components: Pods, Deployments, Services  

Even though NodePort had some limitations due to Windows/Docker Desktop setup, you've found a working path with `port-forward` and `minikube tunnel`.


## 🚀 Next Steps (Optional)

Would you like me to help you:
- Add **ConfigMap** for environment variables  
- Store secrets like `JWT_SECRET_KEY` in **Kubernetes Secrets**
- Create an **Ingress Controller** for multi-app routing  
- Automate deployment with **GitHub Actions**  
- Add **livenessProbe** and **readinessProbe**  
- Write a **Helm chart** for easier installs

Let me know — happy to guide you further into Kubernetes land! 🚀



## 🧾 Done!

You've completed a full Kubernetes deployment journey — from Docker to DevOps-style troubleshooting.

🎉 Great job making it this far! Keep up the awesome work learning Docker and Kubernetes!
