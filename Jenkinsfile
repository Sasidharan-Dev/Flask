pipeline {
    agent any

    environment {
        IMAGE_NAME = "sasidharandevops/tester"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Build Docker Image on Remote') {
            steps {
                sshagent(['docker-cred']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@13.126.16.88 '
                          if [ ! -d ~/app ]; then
                            git clone https://github.com/Sasidharan-Dev/Flask ~/app
                          else
                            cd ~/app && git pull origin main
                          fi

                          cd ~/app
                          docker build -t $IMAGE_NAME:$IMAGE_TAG .
                        '
                    """
                }
            }
        }

        stage('Push Docker Image from Remote') {
            steps {
                sshagent(['docker-cred']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@13.126.16.88 '
                          docker login -u <dockerhub-username> -p <dockerhub-password>
                          docker push $IMAGE_NAME:$IMAGE_TAG
                        '
                    """
                }
            }
        }

        stage('Deploy Container on Remote') {
            steps {
                sshagent(['docker-cred']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@13.126.16.88 '
                          docker ps -q --filter "name=flask-app" | grep -q . && docker stop flask-app && docker rm flask-app || true

                          docker pull $IMAGE_NAME:$IMAGE_TAG
                          docker run -d --name flask-app -p 5000:5000 $IMAGE_NAME:$IMAGE_TAG
                        '
                    """
                }
            }
        }
    }
}
