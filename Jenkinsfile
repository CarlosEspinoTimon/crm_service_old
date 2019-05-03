pipeline {
    agent any


    stages{
        
        stage('Load env variables') {
            steps{
                load "/var/lib/jenkins/envs/crm-staging.groovy"
                
            }
        }

        stage('Tests'){
            steps{
                echo "Running tests..."
            }
        }

        stage('Change yaml') {
            steps{
                script {
                    sh """sed -i "s*PRODUCTION_DATABASE_URI*${env.DATABASE_URI}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_LOGIN_CLIENT_ID*${env.GOOGLE_LOGIN_CLIENT_ID}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_LOGIN_CLIENT_SECRET*${env.GOOGLE_LOGIN_CLIENT_SECRET}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_APPLICATION_CREDENTIALS*${env.GOOGLE_APPLICATION_CREDENTIALS}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_PROJECT*${env.GOOGLE_PROJECT}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh """sed -i "s*YOUR_GOOGLE_BUCKET*${env.GOOGLE_BUCKET}*g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh "cat /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"
                    
                }

            }
        }
        stage('Deploy') {
            steps{
                //Deploy to GCP
                sh """
                    #!/bin/bash 
                    echo "deploy stage";
                    curl -o /tmp/google-cloud-sdk.tar.gz https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-225.0.0-linux-x86_64.tar.gz;
                    tar -xvf /tmp/google-cloud-sdk.tar.gz -C /tmp/;
                    /tmp/google-cloud-sdk/install.sh -q;
                                
                    . /tmp/google-cloud-sdk/path.bash.inc;
                    
                    
                    gcloud config set project ${env.GOOGLE_PROJECT_ID};
                    gcloud auth activate-service-account --key-file ${credentials('service_account_key')};
                    
                    gcloud config list;
                    gcloud app deploy --version=v01;
                    echo "Deployed to GCP"
                """

            }
        }

        
    }


    
   
}