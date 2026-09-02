pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        AWS_ACCOUNT_ID = '943755888791'
        ECR_REPOSITORY = 'aws-devops-app'
        EKS_CLUSTER = 'cloud-native-cluster'

        IMAGE_TAG = "${BUILD_NUMBER}"
        ECR_IMAGE = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_TAG}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify AWS') {
            steps {
                sh '''
                    aws --version
                    aws sts get-caller-identity
                '''
            }
        }

        stage('Terraform Init & Validate') {
            steps {
                dir('terraform') {
                    sh '''
                        terraform init
                        terraform validate
                    '''
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir('terraform') {
                    sh '''
                        terraform plan
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t "$ECR_IMAGE" .
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                    aws ecr get-login-password --region "$AWS_REGION" | \
                    docker login --username AWS \
                    --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push "$ECR_IMAGE"
                '''
            }
        }

        stage('Configure EKS') {
            steps {
                sh '''
                    aws eks update-kubeconfig \
                        --region "$AWS_REGION" \
                        --name "$EKS_CLUSTER"

                    kubectl config current-context
                    kubectl get nodes
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f kubernetes/deployment.yaml
                    kubectl apply -f kubernetes/service.yaml
                '''
            }
        }

        stage('Update Deployment Image') {
            steps {
                sh '''
                    kubectl set image deployment/cloud-native-app \
                        cloud-native-app="$ECR_IMAGE"
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl rollout status deployment/cloud-native-app --timeout=180s
                    kubectl get deployment
                    kubectl get pods
                    kubectl get service
                '''
            }
        }
    }

    post {
        success {
            echo '=========================================='
            echo ' Cloud-Native Deployment Successful!'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo ' Cloud-Native Deployment Failed!'
            echo 'Check the Jenkins console output.'
            echo '=========================================='
        }
    }
}