#!/bin/bash
set -e

BASE_URL="http://127.0.0.1:58402"

echo "Testing health endpoint..."
curl --fail "$BASE_URL/health"

echo "Health OK ✅"

echo "Testing prediction endpoint..."
curl -X POST "$BASE_URL/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg" \
  --fail

echo "Prediction OK ✅"

echo "Smoke test passed 🚀"
