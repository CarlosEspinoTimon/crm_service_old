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
    }


    
   
}