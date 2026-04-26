pipeline {
    agent any
    environment {
        TAG = 'latest'
        repo_name = "weather-app"
        AWS_REGION = "us-east-1"
        AWS_ACCOUNT_ID = "YOUR_AWS_ACCOUNT_ID"
        ECR_URL = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    }
    stages {
        stage('git clone') {
            steps {
                echo 'Cloning the repo'
                git branch: 'main', url: 'https://github.com/YOUR_USERNAME/weather-app.git'
            }
        }
        stage('check docker') {
            steps {
                echo 'Checking docker permission'
                sh 'docker ps'
                sh 'docker images'
            }
        }
        stage('ECR login') {
            steps {
                echo 'Logging into ECR'
                sh 'aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL}'
            }
        }
        stage('building an image') {
            steps {
                echo 'Building docker image'
                sh 'docker build -t ${repo_name}:${TAG} .'
            }
        }
        stage('rename the tag') {
            steps {
                echo 'Tagging image for ECR'
                sh 'docker tag ${repo_name}:${TAG} ${ECR_URL}/${repo_name}:${TAG}'
            }
        }
        stage('push') {
            steps {
                echo 'Pushing to ECR'
                sh 'docker push ${ECR_URL}/${repo_name}:${TAG}'
            }
        }
        stage('deploy') {
            steps {
                echo 'Deploying the container'
                sh 'docker stop weather-app-container || true'
                sh 'docker rm weather-app-container || true'
                sh 'docker run -d -p 5000:5000 --name weather-app-container ${repo_name}:${TAG}'
            }
        }
    }
    post {
        success {
            echo '✅ Pipeline completed successfully! App is live on port 5000.'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs above.'
        }
    }
}
