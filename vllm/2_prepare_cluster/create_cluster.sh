export PROJECT_ID=mlops-405823
export REGION=us-central1

gcloud container clusters create mllmcd-cluster --location ${REGION} \
  --workload-pool ${PROJECT_ID}.svc.id.goog \
  --enable-image-streaming \
  --node-locations=$REGION-a \
  --workload-pool=${PROJECT_ID}.svc.id.goog \
  --machine-type n2d-standard-4 \
  --num-nodes 1 --min-nodes 1 --max-nodes 5 \
  --release-channel=rapid

  gcloud container node-pools create g2-standard-8 --cluster mllmcd-cluster \
  --accelerator type=nvidia-l4,count=1,gpu-driver-version=latest \
  --machine-type g2-standard-8 \
  --enable-autoscaling --enable-image-streaming \
  --num-nodes=0 --min-nodes=0 --max-nodes=3 \
  --node-locations $REGION-a,$REGION-c --region $REGION --spot