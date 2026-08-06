pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
            }
        }
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && python manage.py test'
            }
        }
    }
}
