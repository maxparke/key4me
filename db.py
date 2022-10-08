import boto3
from decimal import Decimal


class LogDb:
    """Encapsulates the DynamoDB table of logs"""

    def __init__(self):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = boto3.resource('dynamodb')
        self.table = self.dyn_resource.Table('location_logs')

    def add_log(self, log):
        item = {
            'call_time': log.call_time.ToJsonString(),
            'car_status': log.car_status,
            'latitude': Decimal(log.latitude),
            'longitude': Decimal(log.longitude),
            'speed': log.speed,
            'recording_sid': log.recording_sid,
            'transcription_sid': log.transcription_sid,
            'call_sid': log.call_sid,
            'raw_text': log.raw_text,
        }
        self.table.put_item(Item=item)
