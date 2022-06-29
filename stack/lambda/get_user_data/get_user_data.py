import json
import boto3
import os

def type_okay(type_code):
  writeable_types = json.loads(os.environ['USER_DATA_READ_TYPES'])
  return type_code in writeable_types

def string_value_from(dynamo_kv):
  return dynamo_kv['S']

def int_value_from(dynamo_kv):
  return dynamo_kv['N']

def string_enc_json_value_from(dynamo_kv):
  s = dynamo_kv['S']
  try:
    return json.loads(s)
  except json.decoder.JSONDecodeError:
    return None
def handler(event, context):
    if not type_okay(event['recordType']):
      raise Exception(f"400_BAD_REQUEST: Type code '{event['recordType']}' is not permitted.")
    else:
      client = boto3.client('dynamodb')
      values = {
        ':typeUserSub': { "S": f"{event['recordType']}::{event['userSub']}" }
      }
      expression = "TypeUserSub = :typeUserSub"
      if event['fromTime'] != '' and event['toTime'] == '':
        expression += " and EpochTime >= :fromTime"
        values[':fromTime'] = { "N" : str(event['fromTime']) }
      elif event['fromTime'] == '' and event['toTime'] != '':
        expression += " and EpochTime <= :toTime"
        values[':toTime'] = { "N" : str(event['toTime']) }
      elif event['fromTime'] != '' and event['toTime'] != '':
        expression += " and EpochTime between :fromTime and :toTime"
        values[':fromTime'] = { "N" : str(event['fromTime']) }
        values[':toTime'] = { "N" : str(event['toTime']) }

      response = client.query(
        TableName = os.environ[ 'DATA_TABLE_NAME' ],
        KeyConditionExpression=expression,
        ExpressionAttributeValues=values
      )
      data = response['Items']
      results = []
      for record in data:
        doc = string_enc_json_value_from(record['Doc']) or string_value_from(record['Doc'])
        r = {
          "Doc": doc,
          "EpochTime": int_value_from(record['EpochTime'])
        }
        results.append(r)

      return {
        'responseStatus': "200_OKAY",
        'body': results,
        'inputEvent': event
      }
