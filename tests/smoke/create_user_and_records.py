#!/usr/bin/env python3

import boto3
from   botocore.exceptions import ClientError
import uuid
import http.client as http_client
from   jwkest.jwt import JWT
from   datetime import datetime
import webbrowser
from   http.server import HTTPServer, BaseHTTPRequestHandler

from tiny_web_server import run_web_server

session = boto3.session.Session()
default_stack_name = 'acme-app-demo'

def value_in_attrs(aws_attribute_list, name):
  value = None
  for attr in aws_attribute_list:
    if attr['Name'] == name:
      value = attr['Value']
      break
  return value
def stack_exports():
  cf_client = session.client('cloudformation')
  exports_result = cf_client.list_exports()
  exports = {}
  for xport in exports_result['Exports']:
    print(f"{ xport['Name'] }::{ xport['ExportingStackId'] }::{ xport['Value'] }")
    if xport['ExportingStackId'].__contains__(f'stack/{default_stack_name}/'):
      exports[xport['Name']] = xport['Value']
  return exports

def exported_var(key):
  prefix = ''.join([ s.capitalize() for s in default_stack_name.split('-')])
  return exported_vars[prefix + '-' + key]

def create_a_user(email, password):
    idp_client = session.client('cognito-idp')
    user_pool_id = exported_var('TheUserPoolId')
    result = idp_client.admin_create_user(
        UserPoolId = user_pool_id,
        Username = email,
        TemporaryPassword = password,
        DesiredDeliveryMediums = ['EMAIL'],
        UserAttributes = [ { 'Name': 'email', 'Value': email } ],
        ValidationData = [ { 'Name': 'email', 'Value': email } ]
    )
    print(result)
    user_sub = value_in_attrs(result['User']['Attributes'], 'sub')
    return user_sub

def decode_tokens(strng):
  jwt = JWT()
  jwt.unpack(strng)
  print("decoded token:")
  print(jwt.payload())

if __name__ == '__main__':
  exported_vars = stack_exports()
  test_email = f'testuser-{uuid.uuid4()}@example.come'
  temp_password = 'Password1!'
  idp_user_sub = create_a_user(test_email, temp_password)
  run_web_server({
    "username": test_email,
    "password": temp_password,
    "userpool_id": exported_var('TheUserPoolId'),
    "userpool_client_id": exported_var('TheUserPoolClientId'),
    "api_url": exported_var('URLOfTheAPI') + 'user-data'
  })

  webbrowser.get('chrome').open_new_tab(f"http://localhost:8765/test_page")

