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
                pkill -f "gunicorn" || true

                # Activate virtual environment
                . venv/bin/activate

                # Start Flask using gunicorn in background
                nohup gunicorn -b 0.0.0.0:5000 app:app > flask.log 2>&1 & disown
                '''
            }
        }

    }
}
