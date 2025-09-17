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
                sh '''
                    pkill -f "flask run" || true
                    . venv/bin/activate
                    nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 & disown
                '''
            }
        }
    }
}
