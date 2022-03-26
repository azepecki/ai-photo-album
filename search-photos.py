import json
import boto3
import requests
from requests_aws4auth import AWS4Auth

lex_client = boto3.client('lex-runtime')
OPEN_SEARCH_URL = 'https://search-photos-veomaryc5keah5aivn3uil4oie.us-east-1.es.amazonaws.com'
credentials = boto3.Session().get_credentials()
region = 'us-east-1'
service = 'es'
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

def call_lex_client(input_text, user_id):
    """Helper function"""
    resp = lex_client.post_text(
        botName='NewPhotoBot',
        botAlias='searchphotos',
        userId='azepecki',
        inputText=input_text,
    )
    print(f"Lex client response=[{resp}]")
    return resp.get('slots')

def search_photos(user_id, query):
    slots = call_lex_client(query, user_id)
    image_urls = []
    for index, tag in slots.items():
        if tag:
            url = f"{OPEN_SEARCH_URL}/photos/_search?q={tag.lower()}"
            print(f"tag=[{tag}] url={[url]}")
            resp = requests.get(url, headers={"Content-Type": "application/json"}, auth=awsauth).json()
            print(f"response=[{resp}]")
            hits = resp.get('hits').get('hits')
            print(f"hits=[{hits}]")
            for photo in hits:
                labels = [l.lower() for l in photo.get('_source').get('labels')]
                if tag in labels:
                    object_key = photo.get('_source').get('objectKey')
                    image_url = f"https://s3.amazonaws.com/amz-a2-b2/{object_key}"
                    image_urls.append(image_url)

    if len(image_urls) > 0:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
				'Content-Type': 'application/json'
			},
            'body': json.dumps(image_urls)
        }
    
    return {
            'statusCode': 200,
            'headers': {
				'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
				'Content-Type': 'application/json'
			},
            'body': {[]}
        } 

def dispatch(event, context):
    """
    Dispatch handles the actually dispatching of the event to the different intent handlers
    """
    query = event.get("queryStringParameters").get("q")
    user_id = event.get("userId")
    print(f"Received request query=[{query}] userId=[{user_id}]")

    return search_photos(user_id, query)

    print(f"Error: Unauthorized intent sent in request: {intent}")

def lambda_handler(event, context):
    """
    Handler looks at the intent and routes to the correct intent
    """
    print(f"Received event: {event}")
    print(f"Event context: {context}")

    return dispatch(event, context)

