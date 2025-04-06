import boto3
import requests

def lambda_handler(event, context):
    # 1. Get the uploaded file info
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']
    print("Received file:", key)

    # 2. Read file from S3
    s3 = boto3.client('s3')
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    text = file_obj['Body'].read().decode('utf-8')

    # 3. Send to summarizer API
    response = requests.post("http://<EC2_IP>/summarize", json={"text": text})
    summary = response.json()['summary']
    print("Summary response:", summary)
    
    # 4. Save summary to S3
    output_key = key.replace('input/', 'output/').replace('.txt', '_summary.txt')
    s3.put_object(Bucket=bucket, Key=output_key, Body=summary.encode('utf-8'))

    return {"status": "ok", "summary_saved_as": output_key}
