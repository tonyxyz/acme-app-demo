from bottle import route, run, template, static_file
import os
import threading

config = {
  "username": "",
  "password": "",
  "userpool_id": "",
  "userpool_client_id": "",
  "api_url": ""
}

@route('/test_page')
def test_page():
  filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_page.tpl')
  return template(filename,
    username=config["username"],
    password=config["password"],
    userpool_id=config["userpool_id"],
    userpool_client_id=config["userpool_client_id"],
    api_url=config["api_url"]
  )

@route('/amazon-cognito-identity.min.js')
def cognito_js():
  root_path = os.path.dirname(os.path.realpath(__file__))
  return static_file('amazon-cognito-identity.min.js', root=root_path)

def start_server():
  run(host='localhost', port=8765)
def run_web_server(cfg):
  global config, server_thread
  config = cfg
  server_thread = threading.Thread(target=start_server)
  server_thread.start()
