export PROJECT_ID=mlops-405823
export REGION=us-central1
export CLUSTER_NAME=mllmcd-cluster

gcloud container clusters delete ${CLUSTER_NAME} --region ${REGION} --quiet