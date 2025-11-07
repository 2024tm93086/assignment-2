pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "flask-app"
        VERSION = "${BUILD_NUMBER}"
        REGISTRY = "2024tm93086"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/2024tm93086/assignment-2.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        // stage('Run Tests') {
        //     steps {
        //         sh 'pytest tests/ -v'
        //     }
        // }
        
        // stage('SonarQube Analysis') {
        //     steps {
        //         script {
        //             def scannerHome = tool 'SonarScanner'
        //             withSonarQubeEnv('sonarqube') {
        //                 sh """
        //                     ${scannerHome}/bin/sonar-scanner \
        //                     -Dsonar.projectKey=flask-app \
        //                     -Dsonar.sources=. \
        //                     -Dsonar.host.url=http://localhost:9000 \
        //                     -Dsonar.python.version=3.11
        //                 """
        //             }
        //         }
        //     }
        // }
        
        // stage('Quality Gate') {
        //     steps {
        //         timeout(time: 1, unit: 'MINUTES') {
        //             waitForQualityGate abortPipeline: true
        //         }
        //     }
        // }
        
        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${DOCKER_IMAGE}:${VERSION} .
                    docker tag ${DOCKER_IMAGE}:${VERSION} ${DOCKER_IMAGE}:latest
                """
            }
        }
        
        stage('Push to Registry') {
            steps {
                script {
                    // Optional: Push to Docker Hub
                    withDockerRegistry([credentialsId: 'dockerhub-credentials', url: '']) {
                        sh """
                            # Tag with registry prefix for version
                            docker tag ${DOCKER_IMAGE}:${VERSION} ${REGISTRY}/${DOCKER_IMAGE}:${VERSION}

                            # Tag with registry prefix for latest
                            docker tag ${DOCKER_IMAGE}:${VERSION} ${REGISTRY}/${DOCKER_IMAGE}:latest

                            # Push both tags
                            docker push ${REGISTRY}/${DOCKER_IMAGE}:${VERSION}
                            docker push ${REGISTRY}/${DOCKER_IMAGE}:latest
                        """
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh """
                    # Stop and remove old container if exists
                    docker stop flask-app-container || true
                    docker rm flask-app-container || true
                    
                    # Run new container
                    docker run -d \
                        --name flask-app-container \
                        -p 5000:5000 \
                        ${DOCKER_IMAGE}:${VERSION}
                """
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            // Clean up workspace
            cleanWs()
        }
    }
}