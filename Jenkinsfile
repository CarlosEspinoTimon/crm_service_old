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
                def filename = '/var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml'
                def data = readYaml file: filename

                // Change something in the file
                data.env_variables.DATABASE_URI = ${env.DATABASE_URI}

                sh "rm $filename"
                writeYaml file: filename, data: data
                
            }
        }

        
    }


    
   
}