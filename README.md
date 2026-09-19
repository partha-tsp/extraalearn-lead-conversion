---
---
title: ExtraaLearn Lead Conversion API
sdk: docker
app_port: 7860
---
---

# ExtraaLearn Lead Conversion API

Flask based REST API for predicting lead conversion for ExtraaLearn.

The API supports both single lead prediction and batch prediction.

## Endpoints

### GET /
Health check endpoint.

### POST /predict
Accepts a single lead and returns the predicted conversion status and conversion probability.

### POST /predict_batch
Accepts multiple leads and returns predictions for all records.
