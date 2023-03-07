import boto3
import os

from db.model import User as User

# dynamodb = boto3.client('dynamodb')
# s3 = boto3.client('s3')
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name="us-east-1" 
)


# --------------- Helper Functions ------------------

def index_faces(image):

    response = rekognition.index_faces(
        Image={'Bytes': image},
        CollectionId="facerecognition_collection",
        MaxFaces=1
    )
    return response
    
# def update_index(tableName,faceId, fullName):
#     response = dynamodb.put_item(
#         TableName=tableName,
#         Item={
#             'RekognitionId': {'S': faceId},
#             'FullName': {'S': fullName}
#             }
#         ) 
    
# --------------- Main handler ------------------

def index_face(image):
    print('Indexing face')
    try:

        # Calls Amazon Rekognition IndexFaces API to detect faces in S3 object 
        # to index faces into specified collection
        response = rekognition.search_faces_by_image(
            CollectionId='facerecognition_collection',
            Image={'Bytes': image}
        )
        for match in response['FaceMatches']:
            print('Rostro conocido')
            if match['Face']['Confidence'] > 99.5:
                try:
                    face = User.get(match['Face']['FaceId'])
                    return {'id': f'{match["Face"]["FaceId"]}', 'register': face}
                except:
                    return {'id': f'{match["Face"]["FaceId"]}', 'register': None}
        response = index_faces(image)
        
        # Commit faceId and full name object metadata to DynamoDB
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            # update_index('facerecognition',faceId,personFullName)

        # Print response to console
        print(response)

        return faceId
    except Exception as e:
        print(e)
        print("Error processing object from bucket")
        raise e