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
                set -e

                # Kill previous Flask process if exists
                if [ -f flask.pid ]; then
                    kill -9 $(cat flask.pid) || true
                    rm -f flask.pid
                fi

                # Activate virtualenv
                . venv/bin/activate

                # Run Flask in background, detached
                nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                echo $! > flask.pid

                echo "Flask started with PID $(cat flask.pid)"
                '''
            }
        }

    }
}
