import json
import pandas as pd
import boto3
def lambda_handler(event, context):
    bucket=event['Records'][0]['s3']['bucket']['name']
    key=event['Records'][0]['s3']['object']['key']
    print("Bucket Name -->",bucket)
    print(key," landed in ",bucket)
    s3_client=boto3.client('s3')
    response=s3_client.get_object(Bucket=bucket,Key=key)
    file_content = response['Body'].read().decode("utf-8")
    data=[]
    for line in file_content.splitlines():
        data_dict = json.loads(line)
        data.append(data_dict)
    df = pd.DataFrame(data)
    filtered_df=df[df['status']=='delivered']
    filtered_dict = filtered_df.to_dict(orient='records')
    dest_bucket='doordash-target-zn-101'
    filename=key
    upload_data = json.dumps(filtered_dict).encode('utf-8')
    s3_client.put_object(Bucket=dest_bucket,Key=filename,Body=upload_data)
    print('Put Complete & SNS notification send via email')
