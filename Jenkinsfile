pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Sasidharan-Dev/Flask.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash
                # Install venv package if not already available
                sudo apt-get update -y
                sudo apt-get install -y python3-venv python3-pip

                # Create venv if missing
                if [ ! -d "venv" ]; then
                  python3 -m venv venv
                fi

                # Activate venv
                . venv/bin/activate

                # Upgrade pip just in case
                pip install --upgrade pip

                # Install requirements inside venv
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Flask') {
            steps {
                sh '''#!/bin/bash
                pkill -f "flask run" || true
                . venv/bin/activate
                nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                '''
            }
        }
    }
}
