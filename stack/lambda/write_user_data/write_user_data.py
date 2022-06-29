import json
import boto3
import os

def type_okay(type_code):
  writeable_types = json.loads(os.environ['USER_DATA_WRITE_TYPES'])
  return type_code in writeable_types
def handler(event, context):
    print(f"event: {json.dumps(event)}")
    if not type_okay(event['recordType']):
      raise Exception(f"400_BAD_REQUEST: Type code '{event['recordType']}' is not permitted.")
    else:
      client = boto3.client('dynamodb')
      client.put_item(TableName = os.environ[ 'DATA_TABLE_NAME' ],
        Item = {
          "TypeUserSub" : { "S" : f"{event['recordType']}::{event['userSub']}" },
          "EpochTime" :   { "N" : event['epochTime'] },
          "Doc" :         { "S" : json.dumps(event['document']) }
        }
      )

      return {
          'responseStatus': "200_OKAY",
          'body': 'Record created.',
          'inputEvent': event
      }