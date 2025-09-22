pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'     // Jenkins credentials ID for DockerHub username/password
        DOCKERHUB_REPO = 'sasidharandevops/tester'         // Replace with your DockerHub repo
        REMOTE_HOST = '13.126.16.88'            // Replace with Docker server IP
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Sasidharan-Dev/Flask'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKERHUB_REPO}:${env.BUILD_NUMBER} ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                      docker push ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Deploy on Docker Server') {
            steps {
                sshagent (credentials: ['docker-cred']) {   // Jenkins SSH private key credentials ID
                    sh """
                      ssh -o StrictHostKeyChecking=no ubuntu@${REMOTE_HOST} '
                        docker pull ${DOCKERHUB_REPO}:${BUILD_NUMBER} &&
                        docker rm -f flask-app || true &&
                        docker run -d --name flask-app -p 5000:5000 --restart unless-stopped ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                      '
                    """
                }
            }
        }
    }
}
