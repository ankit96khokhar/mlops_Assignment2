python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

mlflow:
http://localhost:5050

DVC:
mkdir dvc_storage
dvc init
dvc remote add -d localstorage ./dvc_storage
dvc add data/raw
dvc push


Inference:
uvicorn src.inference:app --host 0.0.0.0 --port 8888

http://localhost:9999/health

Docker:
docker build -t cats-dogs:latest .
docker run -p 9999:9999 cats-dogs:latest


Tests:
python3 -m pytest

Argocd:
argocd login argocd.example.com:8080 --username admin --password ********** --insecure --grpc-web

argocd app create cats-dogs \  --repo https://github.com/ankit96khokhar/mlops_Assignment2.git \
  --path k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
application 'cats-dogs' created

