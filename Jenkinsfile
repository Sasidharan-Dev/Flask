pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Sasidharan-Dev/Flask'
            }
        }

        stage('Setup Venv') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask') {
            steps {
                sh '''#!/bin/bash
                # Kill any previous Flask process if running
                pkill -f "flask run" || true

                # Activate virtual environment
                . venv/bin/activate

                # Start Flask in background, detached from Jenkins
                nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 & disown
                '''
            }
        }

    }
}
