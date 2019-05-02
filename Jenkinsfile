pipeline {
    agent any

    stages{
        stage('Init') {
            steps{
                echo "Funcionaaaa"    
            }
            
        }
        stage('Try env variable') {
            steps{
                echo "bucket=${env.GOOGLE_BUCKET}
                    echo \$bucket"
            }
        }
    }


    
    environment {
        GOOGLE_PROJECT_ID = 'crm-service-238211';
        GOOGLE_SERVICE_ACCOUNT_KEY = credentials('service_account_app_engine');
    }
    

    stage('Deploy'){
        steps{
            
            //Deploy to GCP
            sh """
                #!/bin/bash 
                echo "deploy stage";
                curl -o /tmp/google-cloud-sdk.tar.gz https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-225.0.0-linux-x86_64.tar.gz;
                tar -xvf /tmp/google-cloud-sdk.tar.gz -C /tmp/;
                /tmp/google-cloud-sdk/install.sh -q;
                            
                            source /tmp/google-cloud-sdk/path.bash.inc;
                
                
                    gcloud config set project ${GOOGLE_PROJECT_ID};
                    gcloud components install app-engine-java;
                    gcloud components install app-engine-python;
                    gcloud auth activate-service-account --key-file ${GOOGLE_SERVICE_ACCOUNT_KEY};
                    
                    gcloud config list;
                    gcloud app deploy --version=v01;
                                echo "Deployed to GCP"
            """
            }	
            post{
                always{
                    println "Result : ${currentBuild.result}";
                
                    notifyThroughEmail('Deploy-stage');

                }
        }
    }
}