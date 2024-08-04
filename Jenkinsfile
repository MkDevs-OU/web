pipeline {
    agent any

    environment {
        NETLIFY_BUILD_HOOK_URL = credentials('NETLIFY_BUILD_HOOK_URL')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/MkDevs-OU/web.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh 'python3 -m venv venv' // create a virtual env
                sh '. venv/bin/activate' // activate the virtual env
                sh 'pip install --upgrade pip' // upgrade pip
                sh 'pip install -r requirements.txt' // install dependencies (including Playwright)
                sh 'playwright install' // install Playwright browsers
            }
        }

        stage('Run Playwright Tests') {
            steps {
                sh '. venv/bin/activate' // activate the virtual env
                sh 'pytest tests/' // run your Playwright tests
            }
        }

        stage('Trigger Netlify Deploy') {
            when {
                expression { currentBuild.result == 'SUCCESS' } // only deploy if tests pass
            }
            steps {
                sh 'curl -X POST $NETLIFY_BUILD_HOOK_URL' // trigger Netlify deploy
            }
        }
    }

    post {
        always {
            cleanWs() // clean workspace after build
        }
    }
}
