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

        stage('Run Flask in Background') {
            steps {
                sh '''
                    # Kill old Flask if running
                    if [ -f flask.pid ]; then
                        kill -9 $(cat flask.pid) || true
                        rm -f flask.pid
                    fi

                    . venv/bin/activate
                    export FLASK_APP=app.py

                    # Run Flask in background with nohup
                    nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &

                    # Save the PID
                    echo $! > flask.pid
                    '''
            }
        }
    }
}
