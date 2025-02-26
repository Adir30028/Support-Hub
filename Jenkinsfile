pipeline {
    agent any

    environment {
        DOCKER_IMAGE = env.DOCKER_IMAGE
        DOCKER_TAG = env.DOCKER_TAG
        DOCKER_HUB_USER = env.DOCKER_HUB_USER
        DOCKER_HUB_PASS = env.DOCKER_HUB_PASS
        ANSIBLE_HOST = env.ANSIBLE_HOST
        ANSIBLE_USER = env.ANSIBLE_USER
        SSH_PRIVATE_KEY = env.SSH_PRIVATE_KEY
        GIT_URL = env.GIT_URL
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: "${GIT_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                script {
                    sh "echo ${DOCKER_HUB_PASS} | docker login -u ${DOCKER_HUB_USER} --password-stdin"
                }
            }
        }

        stage('Push Image to DockerHub') {
            steps {
                script {
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                script {
                    writeFile file: 'inventory.ini', text: """
                    [webservers]
                    ${ANSIBLE_HOST} ansible_user=${ANSIBLE_USER} ansible_ssh_private_key_file=/home/jenkins/.ssh/id_rsa
                    """

                    sh """
                    ssh-agent bash -c 'ssh-add /home/jenkins/.ssh/id_rsa && \
                    ansible-playbook -i inventory.ini deploy-playbook.yml'
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline Completed!"
        }
        success {
            echo "Deployment Successful! 🚀"
        }
        failure {
            echo "Something went wrong! ❌"
        }
    }
}
