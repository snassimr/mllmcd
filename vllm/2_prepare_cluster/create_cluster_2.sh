export PROJECT_ID=<your-project-id>
gcloud config set project PROJECT_ID
export PROJECT_ID=$(gcloud config get project)
export REGION=us-central1

gcloud container clusters create l4-demo --location ${REGION} \
  --workload-pool ${PROJECT_ID}.svc.id.goog \
  --enable-image-streaming \
  --node-locations=$REGION-a \
  --workload-pool=${PROJECT_ID}.svc.id.goog \
  --machine-type n2d-standard-4 \
  --num-nodes 1 --min-nodes 1 --max-nodes 5 \
  --release-channel=rapid

  gcloud container node-pools create g2-standard-24 --cluster l4-demo \
  --accelerator type=nvidia-l4,count=2,gpu-driver-version=latest \
  --machine-type g2-standard-24 \
  --enable-autoscaling --enable-image-streaming \
  --num-nodes=0 --min-nodes=0 --max-nodes=3 \
  --node-locations $REGION-a,$REGION-c --region $REGION --spot