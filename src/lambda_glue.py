import json
import boto3

def lambda_handler(event, context):
    # Initialize a boto3 client for AWS Glue
    glue_client = boto3.client('glue')
    
    # Name of your Glue job
    glue_job_name = 'extraction-job'
    
    try:
        # Start the Glue job
        response = glue_client.start_job_run(JobName=glue_job_name)
        
        # Get the JobRunId from the response
        job_run_id = response['JobRunId']
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Glue job started successfully',
                'JobRunId': job_run_id
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error starting Glue job',
                'error': str(e)
            })
        }
    
if __name__ == '__main__':
    event = {}
    context = None
    print(lambda_handler(event, context))