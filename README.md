# Deploy in kubernetes
## Software required
* Cloud google SDK
* Docker
* kubectl (you can download it whit the google SDK)
## Services needed
* Kubernetes
* Artefactory
* Pub/Sub
* Cloud SQL
* Cloud Stoge
* AIM
Create an service account with the permits to pub/sub, cloud SQL, cloud storage
# Create docker repository
```
gcloud artifacts repositories create convert-repo --repository-format=docker --location=us-west2 --description="Docker repository for convert tool"
gcloud auth configure-docker
```
# Create topics and subscription
```
gcloud pubsub topics create email-topic
gcloud pubsub subscriptions create email-topic-sub --topic=email-topic --ack-deadline=120
gcloud pubsub topics create file-topic
gcloud pubsub subscriptions create file-topic-sub --topic=file-topic --ack-deadline=120
```
# Create GCP Instance
Create cluste with autoscaling config
```
gcloud container clusters create convet-cluster-admin --num-nodes=1 --zone=us-east4 --node-locations=us-east4-b,us-east4-c --enable-autoscaling --min-nodes=1 --max-nodes=2 --workload-pool=conversiontoolg34.svc.id.goog
```
# Create and set namespace
```
kubectl create namespace dev-uniandes
kubectl config set-context --current --namespace=dev-uniandes
```
## Create service account 
```
kubectl apply -f service-account.yml
```
### Binding KSA with GSA
In this step is necessary to bind the kubernetes service account with the google service accont 
```
gcloud iam service-accounts add-iam-policy-binding conversiontoolgrupo34@conversiontoolg34.iam.gserviceaccount.com --role="roles/iam.workloadIdentityUser" --member="serviceAccount:conversiontoolg34.svc.id.goog[dev-uniandes/ksa-convert-api]"
```
```
kubectl annotate serviceaccount ksa-convert-api iam.gke.io/gcp-service-account=conversiontoolgrupo34@conversiontoolg34.iam.gserviceaccount.com
```

# Build Docker images
## GCP artifactory
### Create artifactory
```
gcloud artifacts repositories create convert-repo --repository-format=docker --location=us-east4 --description="Docker repository"
```
### Bind docker with artifactory
```
gcloud auth configure-docker us-west2-docker.pkg.dev
``` 
## Build api image
In the api folder run
```
docker build -t us-west2-docker.pkg.dev/conversiontoolgrupo34/convert-repo/convert-api:v1 .
```
When the build finish run 
```
docker push us-west2-docker.pkg.dev/conversiontoolgrupo34/convert-repo/convert-api:v1
```
## Build convet image
In the convert folder run
```
docker build -t us-west2-docker.pkg.dev/conversiontoolgrupo34/convert-repo/convert-batch:v1 .
```
When the build finish run 
```
docker push us-west2-docker.pkg.dev/conversiontoolgrupo34/convert-repo/convert-batch:v1
```
## Build email sender image
In the email sender folder run
```
docker build -t us-west2-docker.pkg.dev/conversiontoolgrupo34/convert-repo/email-sender:v1 .
```
When the build finish run 
```
docker push us-west2-docker.pkg.dev/conversiontoolgrupo34/convert-repo/email-sender:v1
```




kubectl create namespace dev-uniandes

gcloud container node-pools create convert-nodepool --cluster=convet-cluster-admin --workload-metadata=GKE_METADATA

kubectl create serviceaccount ksa-convert-api --namespace dev-uniandes

gcloud iam service-accounts add-iam-policy-binding gsa-convert-api@convertor-tool.iam.gserviceaccount.com --role="roles/iam.workloadIdentityUser" --member="serviceAccount:convertor-tool.svc.id.goog[dev-uniandes/ksa-convert-api]"

kubectl annotate serviceaccount ksa-convert-api --namespace dev-uniandes iam.gke.io/gcp-service-account=gsa-convert-api@convertor-tool.iam.gserviceaccount.com


kubectl autoscale deployment api --cpu-percent=50 --min=1 --max=3 --namespace dev-uniandes