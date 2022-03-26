import json
import boto3
import time
import requests
from requests_aws4auth import AWS4Auth

rekognition_client = boto3.client('rekognition')
OPEN_SEARCH_PHOTOS_INDEX_URL = 'https://search-photos-veomaryc5keah5aivn3uil4oie.us-east-1.es.amazonaws.com/photos/_doc'

region = 'us-east-1' # e.g. us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def lambda_handler(event, context):
    print(f"Event received: [{json.dumps(event)}]")

    record = event.get("Records")[0]
    s3_data = record.get('s3')
    object_key = s3_data.get('object').get('key')
    bucket_name = s3_data.get('bucket').get('name')

    # Call rekognition client to get labels for image
    rek_img = {'S3Object': {'Bucket': bucket_name, 'Name': object_key}}
    resp = rekognition_client.detect_labels(
        Image=rek_img,
        MaxLabels=15
    )
    labels = [l.get('Name') for l in resp.get('Labels')]
    print(f"Labels for image with object_key=[{object_key}]: labels_resp={labels}")

    img = {
        'objectKey': object_key,
        'bucket': bucket_name,
        'createdTimestamp': time.time(),
        'labels': labels,
    }
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(
        OPEN_SEARCH_PHOTOS_INDEX_URL,
        data=json.dumps(img).encode('utf8'),
        auth=awsauth,
        headers=headers
    )
    print(resp)
    print(f"POST to OpenSearch response=[{resp.text}]")

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully added photo to OpenSearch photos')
    }
