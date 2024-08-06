pipeline {
    agent any

    environment {
        NETLIFY_BUILD_HOOK_URL = credentials('NETLIFY_BUILD_HOOK_URL') // Jenkins credentials for Netlify build hook
        DOCKER_IMAGE = 'mcr.microsoft.com/playwright/python:v1.45.1-jammy' // Docker image for Playwright
        SECURE_PROFILE = 'seccomp_profile.json' // path to seccomp profile
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Run Playwright Tests') {
            steps {
                script {
                    // Run tests inside Docker container
                    docker.image(env.DOCKER_IMAGE).inside("--ipc=host --user pwuser --security-opt seccomp=${env.SECURE_PROFILE}") {
                        sh 'pytest --maxfail=1 --disable-warnings -v'
                    }
                }
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
