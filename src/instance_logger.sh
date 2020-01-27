#!/bin/bash

while true
do
  echo "$(date '+%H:%M:%S'),$(gcloud compute instances list --filter="name~w" --uri | wc -l)" | tee -a instances.csv
  sleep 2
done
