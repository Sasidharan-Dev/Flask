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
                sh '''
                if [ ! -d "venv" ]; then
                  python3 -m venv venv
                fi
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run Flask') {
            steps {
                sh '''
                pkill -f "flask run" || true
                nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                '''
            }
        }
    }
}
