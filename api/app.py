from chalice import Chalice
from chalice import CORSConfig
import boto3
import botocore.exceptions


# enable CORS for cross-site API requests
cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)

# set up client objects and instantiate app
ddb = boto3.client('dynamodb')
ddbr = boto3.resource('dynamodb', region_name='us-east-1')
app = Chalice(app_name='equipment-api')


# routes + methods
@app.route('/')
def index():
    return {'routes': ['/laptops']}

@app.route('/laptops', methods=['POST','GET'], cors=cors_config)
def track_laptop():
  request = app.current_request
  if request.method == 'POST':
    laptop_json = app.current_request.json_body
    uid = laptop_json['uid']
    cpu = laptop_json['cpu']
    mem = laptop_json['mem']
    hds = laptop_json['hds']
    try:
      response = ddb.put_item(
          TableName = 'equipment',
          Item={
              'uid': {'S': uid}
              ,'cpu': {'S': cpu}
              ,'mem': {'S': mem}
              ,'hds': {'S': hds}
          }
      )
    except botocore.exceptions.ClientError as e:
      print(e)
    return {"status": 200}
  if request.method == 'GET':
    try:
      table = ddbr.Table('equipment')
      response = table.scan()
      data = response['Items']
      return data
    except botocore.exceptions.ClientError as e:
      print(e)

