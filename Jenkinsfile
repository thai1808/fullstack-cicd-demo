pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "thai1808"
        IMAGE_TAG      = "${env.BUILD_NUMBER}"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
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
            docker run --rm \
                -v /var/run/docker.sock:/var/run/docker.sock \
                -v $WORKSPACE/docker-compose.prod.yml:/deploy/docker-compose.prod.yml \
                -v /root/lab-cicd/.env:/deploy/.env \
                -w /deploy \
                -e IMAGE_TAG=$IMAGE_TAG \
                -e DOCKERHUB_USER=$DOCKERHUB_USER \
                docker:27-cli \
                sh -c "docker compose --env-file .env -f docker-compose.prod.yml pull && docker compose --env-file .env -f docker-compose.prod.yml up -d"
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
