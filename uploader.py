import boto3


class Uploader:
    """Encapsulates uploading logic for s3"""

    def __init__(self):
        self.s3_client = boto3.client('s3')

    def write_new_index(self, content):
        self.s3_client.put_object(Bucket="key4me.xyz",
                                  Key="index.html",
                                  ContentType="text/html",
                                  Body=bytes(content, 'utf-8'))
