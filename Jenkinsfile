pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "flask-app"
        VERSION = "${BUILD_NUMBER}"
        REGISTRY = "2024tm93086"
        AWS_REGION = 'ap-south-1'
        EKS_CLUSTER_NAME = 'bits-assignment-2'
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
        
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('sonarqube') {
                        sh """
                            . .venv/bin/activate
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=flask-app \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.python.version=3.11
                        """
                    }
                }
            }
        }
        
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

        stage('Configure kubectl for EKS') {
            steps {
                sh """
                    echo "Configuring kubectl for EKS cluster: ${EKS_CLUSTER_NAME}"
                    
                    # Update kubeconfig
                    aws eks update-kubeconfig \
                        --region ${AWS_REGION} \
                        --name ${EKS_CLUSTER_NAME}
                    
                    # Verify connection
                    kubectl cluster-info
                    kubectl get nodes
                """
            }
        }

        stage('Update Kubernetes Manifests') {
            steps {
                sh """
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl get pods
                    kubectl get svc
                """
            }
        }

        
        // stage('Deploy') {
        //     steps {
        //         sh """
        //             # Stop and remove old container if exists
        //             docker stop flask-app-container || true
        //             docker rm flask-app-container || true
                    
        //             # Run new container
        //             docker run -d \
        //                 --name flask-app-container \
        //                 -p 5000:5000 \
        //                 ${DOCKER_IMAGE}:${VERSION}
        //         """
        //     }
        // }
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
            sh 'kubectl get all -A | head -n 50 || true'
            cleanWs()
        }
    }
}