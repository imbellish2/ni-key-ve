# NiKeyVe

Key-value store built in AWS Lambda

### Quick note
All of the CRUD functions are contained in a single file ```nikeyve.py``` for (IMO) easier browsing. 

### Deployment


```
serverless deploy --verbose
```

### REST API endpoints
Listed here are the current live endpoints for the key value store. 

```
GET - https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/status
Response:
{
	"status": "ok"
}
Example:
curl -XGET https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/status
```

POSTs and PUTs require a key and value, where the key is in the URL and the value is in a JSON object such as 
```
{
	"data: <value: pretty much anything you want>
}
```
Create a new key-value pair:
```
POST - https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/create/{id}
Response:
{
	"{id}": <value>
}
Example:
curl -XPOST https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/create/testobject --data '{"data": [1, 2, 3]}'
```
You can verify the above post with a GET to /key/{id}
```
GET - https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/key/{id}
Response:
{
	"{id}": <value>
}
curl -XGET https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/key/testobject
```
And you can retrieve all keys with a GET to /keys/
```
GET - https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/keys
Response:
{
	"keys": [{key-value pair}, {key-value pair}, {...}]
}
```
Updates will return a 404 if the object has not been created yet. 

```
PUT - https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/key/{id}
Response:
{
	"{id}": <value>
}
Example:
# expected failure
python3 -c "import uuid; print(str(uuid.uuid4()))" \
     	| curl -XPUT https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/key/@- \
    	-d '{"data": "expected 404"}'
# expected success
curl -XPUT https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/key/testobject -d '{"data": "expected success!"}'
```
Deleting mimics the behavior of DynamoDB in that it always returns a 200, even if the object did not exist.
```
DELETE - https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/key/{id}
Response: None
Example:
curl -XDELETE https://utomwfr2t5.execute-api.us-west-2.amazonaws.com/dev/key/testobject
```
  


### Testing

#### Unit

Make sure DynamoDB is running locally. There are warnings from the boto3 lib about sockets not being closed, so optionally suppress those warnings by passing the ```-W ignore``` flag.
```
python3 -W ignore test.py
```