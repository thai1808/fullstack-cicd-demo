pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "thai1808"
        IMAGE_TAG      = "${env.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        DEPLOY_DIR     = "/root/lab-cicd"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Test Backend') {
            steps {
                sh '''
                    docker run --rm -v $WORKSPACE/backend:/app -w /app python:3.12-slim \
                        bash -c "pip install -r requirements.txt -q && pytest -q --junitxml=result.xml"
                '''
            }
            post {
                always { junit 'backend/result.xml' }
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                    docker build -t $DOCKERHUB_USER/fullstack-backend:$IMAGE_TAG -t $DOCKERHUB_USER/fullstack-backend:latest ./backend
                    docker build -t $DOCKERHUB_USER/fullstack-frontend:$IMAGE_TAG -t $DOCKERHUB_USER/fullstack-frontend:latest ./frontend
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker push $DOCKERHUB_USER/fullstack-backend:$IMAGE_TAG
                    docker push $DOCKERHUB_USER/fullstack-backend:latest
                    docker push $DOCKERHUB_USER/fullstack-frontend:$IMAGE_TAG
                    docker push $DOCKERHUB_USER/fullstack-frontend:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    cp docker-compose.prod.yml $DEPLOY_DIR/docker-compose.prod.yml
                    cd $DEPLOY_DIR
                    export IMAGE_TAG=$IMAGE_TAG
                    docker compose --env-file .env -f docker-compose.prod.yml pull
                    docker compose --env-file .env -f docker-compose.prod.yml up -d
                    docker image prune -f
                '''
            }
        }
    }

    post {
        success { echo "✅ Deploy thành công! Truy cập: http://<VPS_IP>:9280" }
        failure { echo "❌ Pipeline thất bại — kiểm tra log." }
    }
}
