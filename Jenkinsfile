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
                echo """bucket=${env.GOOGLE_BUCKET}
                    echo \$bucket"""
            }
        }
        stage('Where') {
            steps{
                echo """echo Shell $PWD"""
            }
        }

        stage("Source activate") {
            steps{
                echo """echo cd /var/lib/jenkins/envs/"""
                echo """echo source .env """
                echo "echo \$GOOGLE_PROJECT"
            }
        }
    }


    
   
}