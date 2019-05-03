pipeline {
    agent any

    stages{
        stage('Init') {
            steps{
                echo "Funcionaaaa"    
            }
            
        }
        stage('Load env variables') {
            steps{
                load "/var/lib/jenkins/envs/crm-staging.groovy"
            }
        }
        stage('Where') {
            steps{
                echo """echo Shell $PWD"""
            }
        }

        stage('Change yaml') {
            steps{
                script {
                    def inptext = readFile file: '/var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml' 
                    inptext = inptext.replaceAll("PRODUCTION_DATABASE_URI", "${env.DATABASE_URI}")       
                    inptext = inptext.replaceAll("YOUR_GOOGLE_LOGIN_CLIENT_ID", "${env.GOOGLE_LOGIN_CLIENT_ID}")       
                    inptext = inptext.replaceAll("YOUR_GOOGLE_LOGIN_CLIENT_SECRET", "${env.GOOGLE_LOGIN_CLIENT_SECRET}")       
                    inptext = inptext.replaceAll("YOUR_GOOGLE_APPLICATION_CREDENTIALS", "${env.GOOGLE_APPLICATION_CREDENTIALS}")       
                    inptext = inptext.replaceAll("YOUR_GOOGLE_PROJECT", "${env.GOOGLE_PROJECT}")       
                    inptext = inptext.replaceAll("YOUR_GOOGLE_BUCKET", "${env.GOOGLE_BUCKET}")       
                    writeFile file: "'/var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml'", text: inptext
                    
            
                    sh "cat /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"
                    sh """sed -i "s/PRODUCTION_DATABASE_URI/${env.DATABASE_URI}/g" /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"""
                    sh "cat /var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml"
                    
                }

            }
        }

        
    }


    
   
}