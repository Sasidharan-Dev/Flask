pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'     // Jenkins credentials ID for DockerHub
        DOCKERHUB_REPO = 'sasidharandevops/tester'    // Replace with your DockerHub repo
        REMOTE_HOST = '13.126.16.88'            // Replace with Docker server IP
    }

    stages {
        stage('Build Docker Image on Remote') {
            steps {
                sshagent (credentials: ['docker-cred']) {
                    sh """
                      ssh -o StrictHostKeyChecking=no ubuntu@${REMOTE_HOST} '
                        # prepare app folder
                        if [ ! -d ~/app ]; then
                          git clone https://github.com/Sasidharan-Dev/Flask ~/app
                        else
                          cd ~/app && git pull origin main
                        fi

                        cd ~/app
                        docker build -t ${DOCKERHUB_REPO}:${BUILD_NUMBER} .
                      '
                    """
                }
            }
        }

        stage('Push Docker Image from Remote') {
            steps {
                sshagent (credentials: ['docker-cred']) {
                    sh """
                      ssh -o StrictHostKeyChecking=no ubuntu@${REMOTE_HOST} '
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                      '
                    """
                }
            }
        }

        stage('Deploy Container on Remote') {
            steps {
                sshagent (credentials: ['docker-cred']) {
                    sh """
                      ssh -o StrictHostKeyChecking=no ubuntu@${REMOTE_HOST} '
                        docker rm -f flask-app || true
                        docker run -d --name flask-app -p 5000:5000 --restart unless-stopped ${DOCKERHUB_REPO}:${BUILD_NUMBER}
                      '
                    """
                }
            }
        }
    }
}
