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
                    writeFile file: "'/var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml'", text: inptext
                    
                    // def filename = '/var/lib/jenkins/workspace/crm_pipeline/backend/app.yaml'
                    // def data = readYaml file: filename

                    // // Change something in the file
                    // data.env_variables.PRODUCTION_DATABASE_URI = ${env.DATABASE_URI}

                    // sh "rm $filename"
                    // writeYaml file: filename, data: data
                    
                }

            }
        }

        
    }


    
   
}