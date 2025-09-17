pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Sasidharan-Dev/Flask'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash
                # Create venv if missing
                if [ ! -d "venv" ]; then
                  python3 -m venv venv
                fi

                # Activate venv
                . venv/bin/activate

                # Upgrade pip just in case
                pip install --upgrade pip

                # Install requirements inside venv
                pip install -r requirements.txt --break-system-packages || true
                '''
            }
        }

        stage('Run Flask') {
            steps {
                sh '''#!/bin/bash
                pkill -f "flask run" || true
                . venv/bin/activate
                export FLASK_APP=app.py
                nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                sleep 5
                ps -ef | grep "flask run" | grep -v grep
                '''
            }
        }
    }
}
