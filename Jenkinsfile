pipeline {
    agent any

    environment {
        VENV_DIR = 'venv' // Define the virtual environment directory
        LOCAL_BIN = '/var/lib/jenkins/.local/bin'
        NETLIFY_BUILD_HOOK_URL = credentials('NETLIFY_BUILD_HOOK_URL') // Use Jenkins credentials for security
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
                    // Create and activate Python virtual environment
                    sh "python3 -m venv ${env.VENV_DIR}"
                    sh '''
                    . ${env.VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Install Playwright') {
            steps {
                script {
                    // Ensure the local bin directory is in PATH
                    sh '''
                    . ${env.VENV_DIR}/bin/activate
                    export PATH="${env.LOCAL_BIN}:${PATH}"
                    playwright install
                    '''
                }
            }
        }

        stage('Run Playwright Tests') {
            steps {
                script {
                    // Run Playwright tests
                    sh '''
                    . ${env.VENV_DIR}/bin/activate
                    export PATH="${env.LOCAL_BIN}:${PATH}"
                    playwright test
                    '''
                }
            }
        }

        stage('Trigger Netlify Deploy') {
            when {
                expression { currentBuild.result == 'SUCCESS' } // Only deploy if tests pass
            }
            steps {
                sh 'curl -X POST $NETLIFY_BUILD_HOOK_URL' // Trigger Netlify deploy
            }
        }

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }
    }

    post {
        failure {
            echo 'Build failed. Please check the logs for details.'
        }
        success {
            echo 'Build succeeded!'
        }
        always {
            echo 'Cleaning up...'
            cleanWs()
        }
    }
}
