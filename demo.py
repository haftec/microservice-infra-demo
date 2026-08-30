import os
import boto3
from http.server import HTTPServer, BaseHTTPRequestHandler

LOCALSTACK_ENDPOINT = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")

# Making the connection with LocalStack
s3_client = boto3.client(
    's3',
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name='us-east-1',
    aws_access_key_id='mock_key',
    aws_secret_access_key='mock_secret'
)

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=LOCALSTACK_ENDPOINT,
    region_name='us-east-1',
    aws_access_key_id='mock_key',
    aws_secret_access_key='mock_secret'
)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Add a record to DynamoDB and upload a file to S3 on every GET request
            table = dynamodb.Table('microservice-logs')
            table.put_item(Item={'LogID': 'REQ_001', 'Status': 'HTTP GET Received'})
            s3_client.put_object(Bucket='microservice-storage-bucket', Key='last_request.txt', Body='GET request handled')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"Hello from Microservice! LocalStack Integration Active.")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

if __name__ == '__main__':
    # Allow immediate port reuse to avoid Errno 98 error
    HTTPServer.allow_reuse_address = True
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()