pipeline {
    agent any

    environment {
        NETLIFY_TOKEN = credentials('NETLIFY_TOKEN')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/MkDevs-OU/web.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '. venv/bin/activate'
                sh 'pytest tests'
            }
        }

        stage('Install Netlify CLI') {
            steps {
                sh 'npm install -g netlify-cli'
            }
        }

        stage('Deploy to Netlify') {
            when {
                expression { currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'NETLIFY_TOKEN', variable: 'NETLIFY_TOKEN')]) {
                        sh 'netlify deploy --prod --dir=dist'
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs() // clean workspace after build
        }
    }
}
