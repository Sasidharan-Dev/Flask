pipeline {
    agent any

    environment {
        REMOTE_USER   = "ubuntu"                // Lightsail default username
        REMOTE_HOST   = "3.109.185.129"    // Replace with your Docker server IP
        SSH_CRED_ID   = "server-cred"        // Jenkins SSH credential ID (PEM key)
        DOCKERHUB_REPO = "sasidharandevops/tester" // e.g. myuser/myflask
        DOCKERHUB_CRED_ID = "dockerhub-cred"   // Jenkins Docker Hub credentials ID
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
                    sh """
                        ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} '
                            set -e

                            # Create app directory if not exists
                            mkdir -p ~/flask_app

                            # Clean old files
                            rm -rf ~/flask_app/*

                            # Exit shell
                        '
                    """

                    // Copy repo files to Docker server
                    sh """
                        scp -o StrictHostKeyChecking=no -r * ${env.REMOTE_USER}@${env.REMOTE_HOST}:~/flask_app/
                    """

                    // Build + Push + Deploy on remote Docker server
                    sshagent (credentials: [env.SSH_CRED_ID]) {
                        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CRED_ID, usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                            sh """
                                ssh -o StrictHostKeyChecking=no ${env.REMOTE_USER}@${env.REMOTE_HOST} '
                                    cd ~/flask_app

                                    # Get short commit hash for tag
                                    TAG=$(git rev-parse --short HEAD || date +%s)
                                    IMAGE=${env.DOCKERHUB_REPO}:\$TAG

                                    echo "Building image \$IMAGE"

                                    # Docker login with Jenkins-provided creds
                                    echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin

                                    # Build and push image
                                    docker build -t \$IMAGE .
                                    docker push \$IMAGE

                                    # Stop old container if exists
                                    docker rm -f ${env.APP_NAME} || true

                                    # Run new container
                                    docker run -d --name ${env.APP_NAME} -p 5000:5000 --restart unless-stopped \$IMAGE
                                '
                            """
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Flask app deployed successfully on Docker server."
        }
        failure {
            echo "❌ Build or deploy failed. Check logs."
        }
    }
}
