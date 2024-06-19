from chalice import Chalice
import boto3

ddb = boto3.client('dynamodb')
ddbr = boto3.resource('dynamodb', region_name='us-east-1')
app = Chalice(app_name='equipment-api')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/laptops', methods=['POST','GET'])
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
    except Exception as e:
      print(e)
    return {"status": 200}
  if request.method == 'GET':
    try:
      table = ddbr.Table('equipment')
      response = table.scan()
      data = response['Items']
      return data
    except Exception as e:
      print(e)

