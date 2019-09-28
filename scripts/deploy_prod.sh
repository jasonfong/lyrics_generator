#! /bin/bash

gcloud app deploy \
  --no-promote \
  --project $GCP_PROJ_PROD
