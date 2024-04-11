# elementor-assignment
For this project i used kind cluster because its lightweight and flexible

I used it on my linux and windows machines it should work on Mac also


# Prerequisites
[docker](https://docs.docker.com/engine/install/)

[helm](https://helm.sh/docs/intro/install/)

[kubectl](https://kubernetes.io/docs/tasks/tools/)

git clone the repo

# For local Tests with docker only
```
docker compose --file Application/docker-compose.yaml up -d
```

test it
```
curl http://localhost:8080/health
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
```


## Install both services
```
helm upgrade --install elementor-assignment Kubernetes/
```

After one minute because the nginx controller takes a few seconds to be ready you can try to access the endpoints

```
curl http://localhost/health
curl http://localhost/get_details
```


## NOTES
- In order to convert the original script to the REST application, i put the csv writer inside the get_humanoid_characters_details() so you could see i did the first task

- Why i dont limit my cpu on the pod's containers(Its very interesting) -> https://medium.com/directeam/kubernetes-resources-under-the-hood-part-3-6ee7d6015965

If you have any questions or wonders feel free to ask me what and why i did

Enjoy and Thank you!
