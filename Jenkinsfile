pipeline {
    agent any

    environment {
        TAG            = 'latest'
        repo_name      = "weather-app"
        AWS_REGION     = "eu-north-1"
        AWS_ACCOUNT_ID = "173194475207"
        ECR_URL        = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_FULL     = "${ECR_URL}/${repo_name}:${TAG}"
    }

    stages {

        stage('Git Clone') {
            steps {
                echo '===== Cloning GitHub Repo ====='
                git branch: 'main',
                    url: 'https://github.com/shivaninwalekar/weather-app.git'
            }
        }

        stage('Check Docker') {
            steps {
                echo '===== Checking Docker Access ====='
                sh 'docker ps'
                sh 'docker images'
            }
        }

        stage('ECR Login') {
            steps {
                echo '===== Logging into AWS ECR ====='
                sh '''
                    aws ecr get-login-password --region eu-north-1 \
                    | docker login --username AWS \
                      --password-stdin 173194475207.dkr.ecr.eu-north-1.amazonaws.com
                '''
            }
        }

        stage('Build Image') {
            steps {
                echo '===== Building Docker Image ====='
                sh '''
                    ls -la
                    cat Dockerfile
                    docker build -t ${repo_name}:${TAG} .
                '''
            }
        }

        stage('Tag Image') {
            steps {
                echo '===== Tagging Image for ECR ====='
                sh 'docker tag ${repo_name}:${TAG} ${IMAGE_FULL}'
            }
        }

        stage('Push to ECR') {
            steps {
                echo '===== Pushing Image to ECR ====='
                sh 'docker push ${IMAGE_FULL}'
            }
        }

        stage('Deploy Container') {
            steps {
                echo '===== Deploying Weather App ====='
                sh '''
                    docker stop weather-app-container || true
                    docker rm   weather-app-container || true
                    docker run -d \
                        -p 5000:5000 \
                        --name weather-app-container \
                        --restart always \
                        ${repo_name}:${TAG}
                '''
            }
        }
    }

    post {
        success {
            echo '✅ SUCCESS — Weather App live at http://16.16.91.176:5000'
        }
        failure {
            echo '❌ FAILED — Check the red stage above for the error'
        }
        always {
            sh 'docker image prune -f || true'
        }
    }
}
