pipeline {
    agent any

    environment {
        REMOTE_USER   = "ubuntu"
        REMOTE_HOST   = "3.109.185.129"
        SSH_CRED_ID   = "server-cred"
        DOCKERHUB_REPO = "sasidharandevops/tester"
        DOCKERHUB_CRED_ID = "dockerhub-cred"
        APP_NAME = "flask-app"
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Build, Push, and Deploy on Docker Server') {
            steps {
                sshagent (credentials: [env.SSH_CRED_ID]) {
                    // prepare folder
                    sh """
                        ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} '
                            mkdir -p ~/flask_app && rm -rf ~/flask_app/*
                        '
                    """

                    // copy files
                    sh """
                        scp -o StrictHostKeyChecking=no -r * ${env.REMOTE_USER}@${env.REMOTE_HOST}:~/flask_app/
                    """

                    // build & deploy
                    withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CRED_ID, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} '
                                cd ~/flask_app
                                TAG=\$(git rev-parse --short HEAD || date +%s)
                                IMAGE=${DOCKERHUB_REPO}:\$TAG

                                echo "Building image \$IMAGE"
                                echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin

                                docker build -t \$IMAGE .
                                docker push \$IMAGE

                                docker rm -f ${APP_NAME} || true
                                docker run -d --name ${APP_NAME} -p 5000:5000 --restart unless-stopped \$IMAGE
                            '
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Flask app deployed successfully."
        }
        failure {
            echo "❌ Build or deploy failed. Check logs."
        }
    }
}
