import os
import re
from twilio.rest import Client
from key4me_pb2 import LocationLog
from google.protobuf.timestamp_pb2 import Timestamp

MY_PHONE = "+19259408556"


def get_client():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    return Client(account_sid, auth_token)


def make_call(number_to_notify):
    domain = "https://59dc-100-37-221-219.ngrok.io/"
    callback_url = domain + "transcription_callback/"
    if number_to_notify is not None:
        callback_url += number_to_notify
    remote_phone = "+13375394255"
    twiml = "<Response><Record transcribe='true' timeout='10' transcribeCallback='{}'/></Response>".format(
        callback_url)
    print(twiml)
    call = get_client().calls.create(twiml=twiml,
                                     to=remote_phone,
                                     from_=MY_PHONE)
    return call.sid


def fetch_transcript():
    [transcription] = get_client().transcriptions.list(limit=1)
    recording = get_client().recordings.get(transcription.recording_sid).fetch()
    call = get_client().calls.get(recording.call_sid).fetch()
    return parse_transcript(transcription, recording, call)


def parse_transcript(transcription, recording, call):
    transcription_text = transcription.transcription_text
    log = LocationLog()
    log.call_time.FromDatetime(call.end_time)
    log.transcription_sid = transcription.sid
    log.recording_sid = recording.sid
    log.call_sid = call.sid
    log.raw_text = transcription_text

    coordinates = re.findall("([0-9]+\.[0-9]+)", transcription_text)
    if len(coordinates) == 2:
        [raw_latitude, raw_longitude] = coordinates
        longitude = -float(raw_longitude)
        latitude = float(raw_latitude)
        log.latitude = latitude
        log.longitude = longitude
    else:
        print("Coordinates not found in transcript: " + transcription_text)

    statuses = re.findall("currently moving|currently not moving",
                          transcription_text)
    if len(statuses) == 1:
        if statuses[0] == "currently moving":
            log.car_status = LocationLog.CarStatus.MOVING
        elif statuses[0] == "currently not moving":
            log.car_status = LocationLog.CarStatus.STOPPED
    else:
        print("Status not found in transcript: " + transcription_text)

    speeds = re.findall("([0-9]+) miles per hour", transcription_text)
    if len(speeds) == 1:
        log.speed = float(speeds[0])
    elif log.car_status == LocationLog.CarStatus.STOPPED:
        log.speed = 0
    else:
        print("Speed not found in transcript: " + transcription_text)

    return log

def send_text(number, content):
    message = get_client().messages \
            .create(
                 body=content,
                 from_=MY_PHONE,
                 to=number
             )
