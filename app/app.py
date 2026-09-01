from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Scalable Cloud-Native Application is Running!"

@app.route("/health")
def health():
    return "Application is healthy"

@app.route("/info")
def info():
    return {
        "application": "Cloud Native Application",
        "platform": "AWS EKS",
        "container": "Docker",
        "orchestration": "Kubernetes"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)