# elementor-assignment
For this project i used kind cluster because its lightweight and flexible

I used it on my linux and windows machines it should work on Mac also


# Prerequisites
[docker](https://docs.docker.com/engine/install/)

[helm](https://helm.sh/docs/intro/install/)

[kubectl](https://kubernetes.io/docs/tasks/tools/)

git clone the repo

# For local Tests without docker
Created a RESTful webapp in python with enpoints /get_details and /healthcheck

Windows:
```
python Application/app.py
```

Linux/Mac:
```
python3 Application/app.py
```

Test it
```
curl localhost:8080//healthcheck
curl localhost:8080/get_details
```

# For local Tests with docker only
can build with buildx:
```
docker buildx build --load -t rick-and-morty Application 
```

Or docker compose:
```
docker compose --file Application/docker-compose.yaml up -d
```

test it
```
curl http://localhost:8080/healthcheck
curl http://localhost:8080/get_details
```

# For Local Kubernetes

## To download

Reference from https://kind.sigs.k8s.io/docs/user/quick-start/#installing-with-a-package-manager

Mac:

```
brew install kind
```

Linux:
```
# For AMD64 / x86_64
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
# For ARM64
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-arm64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Windows:
```
choco install kind
```

## Create a kind cluster with the following configuration in order for us to reach the cluster from the localhost(make sure port 80 is available), on windows use git bash
```
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
EOF
```


## Then make sure to use the cluster
```
kubectl config use-context kind-kind
```


## Install nginx ingress controller with the following configuration
```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

helm upgrade --install -n kube-system ingress-nginx ingress-nginx/ingress-nginx \
    --set controller.hostPort.enabled=true \
    --set controller.admissionWebhooks.enabled=false

kubectl -n kube-system wait --for=condition=ready pod -l app.kubernetes.io/name=ingress-nginx
```

After one minute because the nginx controller takes a few seconds to be ready you can try to access the endpoints

## Install service with yamls
```
kubectl apply -f yamls/
```

```
curl http://localhost/healthcheck
curl http://localhost/get_details
```



## Install service with Helm
```
helm upgrade --wait --install rick-and-morty Helm/
```

```
curl http://localhost/healthcheck
curl http://localhost/get_details
```


## GitHub Actions Workflow: CI-CD Pipeline
This CI-CD pipeline automates the process of building, testing, and deploying applications using Docker and Kubernetes. It is triggered on any push or pull request to the main branch.

### Workflow
1. Checkout Repository: Clones the code for access by subsequent steps.

2. Set up Docker Buildx: Prepares the environment for building Docker images with Buildx for advanced features.

3. Login to Docker Registry: Authenticates to Docker Hub to enable image push capabilities using secured credentials.

4. Build and Push Docker Image: Constructs the Docker image from the Application/ directory and pushes it to a Docker Hub repository with a different tag version every run .

5. Create k8s Kind Cluster: Initializes a Kubernetes cluster using Kind, configured via Application/kind-config.yaml.

6. Installing NGINX Ingress: Deploys NGINX Ingress in the cluster to manage external access to services.

7. Deploy to Kubernetes: Applies Kubernetes manifests using Helm from the Helm/ directory to deploy the application.

7. Run Tests: Executes end-to-end tests to verify the deployment, retrying up to 5 times in case of failures.

### Concurrency
This pipeline ensures that only the latest run is processed at any time by cancelling any in-progress runs when a new run is triggered.

### Execution
Push changes to the main branch or open a pull request targeting main to initiate the workflow.

## NOTES
- In order to convert the original script to the REST application, i put the csv writer inside the get_humanoid_characters_details() so you could see i did the first task

- Why i dont limit my cpu on the pod's containers(Its very interesting) -> https://medium.com/directeam/kubernetes-resources-under-the-hood-part-3-6ee7d6015965

If you have any questions or wonders feel free to ask me what and why i did

Enjoy and Thank you!
