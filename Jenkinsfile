pipeline {
    agent any

    environment {
	    GOOGLE_SERVICE_ACCOUNT_KEY = credentials('deployment_key');
    }

    stages{

        
        stage('Load env variables') {
            steps{
                load "/var/lib/jenkins/envs/crm-staging.groovy"
                checkout scm

                echo "branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Tests'){
            steps{
                echo "Build environment"
                sh "docker-compose -f /var/lib/jenkins/workspace/crm_pipeline/docker-compose.yaml build"
                sh "docker-compose -f /var/lib/jenkins/workspace/crm_pipeline/docker-compose.yaml up -d"
                echo "Execute initial dump script"
                sh "mysql -u root -h 127.0.0.1  -proot_super_password < initial_dump_test.sql"
                echo "Running tests..."
                sh "docker exec -i crm_pipeline_crm_backend_1 pipenv run python tests.py"
            }
        }

        // stage('Change yaml') {
        //     steps{
        //         script {
        //             sh """sed -i "s*PRODUCTION_DATABASE_URI*${env.DATABASE_URI}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
        //             sh """sed -i "s*YOUR_GOOGLE_LOGIN_CLIENT_ID*${env.GOOGLE_LOGIN_CLIENT_ID}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
        //             sh """sed -i "s*YOUR_GOOGLE_LOGIN_CLIENT_SECRET*${env.GOOGLE_LOGIN_CLIENT_SECRET}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
        //             sh """sed -i "s*YOUR_GOOGLE_APPLICATION_CREDENTIALS*${env.GOOGLE_APPLICATION_CREDENTIALS}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
        //             sh """sed -i "s*YOUR_GOOGLE_PROJECT*${env.GOOGLE_PROJECT}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
        //             sh """sed -i "s*YOUR_GOOGLE_BUCKET*${env.GOOGLE_BUCKET}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
        //             sh "cat /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"
                    
        //         }

        //     }
        // }
      
        stage('Deploy to GCP') {
            when {
                branch "master" 
            } 
            steps{
                echo "Modify yaml"
                script {
                    sh """sed -i "s*PRODUCTION_DATABASE_URI*${env.DATABASE_URI}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_LOGIN_CLIENT_ID*${env.GOOGLE_LOGIN_CLIENT_ID}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_LOGIN_CLIENT_SECRET*${env.GOOGLE_LOGIN_CLIENT_SECRET}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_APPLICATION_CREDENTIALS*${env.GOOGLE_APPLICATION_CREDENTIALS}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_PROJECT*${env.GOOGLE_PROJECT}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_BUCKET*${env.GOOGLE_BUCKET}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh "cat /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"
                    
                }
                echo "Generate requirements.txt"
                sh "docker exec -i crm_pipeline_crm_backend_1 pipenv lock -r > requirements.txt"
                sh "echo \"gunicorn==19.3.0\" >> requirements.txt"
                echo "Remove first line"
                sh "echo \"\$(tail -n +2 requirements.txt)\" > requirements.txt"
                echo "Deploy"
                // sh """ 
                //     #!/bin/bash
                //     echo "Deploy stage";
                //     curl -o /tmp/google-cloud-sdk.tar.gz https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-225.0.0-linux-x86_64.tar.gz;
                //     tar -xvf /tmp/google-cloud-sdk.tar.gz -C /tmp/;
                //     /tmp/google-cloud-sdk/install.sh -q;
                                
                //     . /tmp/google-cloud-sdk/path.bash.inc;
                    
                    
                //     gcloud config set project ${env.GOOGLE_PROJECT};
                //     gcloud auth activate-service-account --key-file ${GOOGLE_SERVICE_ACCOUNT_KEY};
                    
                //     gcloud config list;
                //     gcloud app deploy /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml;
                //     echo "Deployed to GCP"
                // """

            }
        }
        stage('Clean up') {
            steps{
                echo "Stop all containers"
                sh "docker stop \$(docker ps -a -q)"
                // echo "Delete all containers"
                // sh "docker rm \$(docker ps -a -q)"
                // echo "Delete all images"
                // sh "docker rmi \$(docker images -q)"
            }
        }

        
    }


    
   
}