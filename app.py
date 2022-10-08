from flask import Flask
from google.protobuf import text_format
import key4me
import phonenumbers

app = Flask(__name__)


@app.route("/make_call/<number_to_notify>")
def make_call(number_to_notify=None):
    if number_to_notify is not None:
        n = phonenumbers.parse(number_to_notify, "US")
        if phonenumbers.is_valid_number(n):
            number_to_notify = phonenumbers.format_number(
                n, phonenumbers.PhoneNumberFormat.E164)
    sid = key4me.make_call(number_to_notify)
    print("CALL SID: {} NOTIFICATION NUMBER: {}".format(sid, number_to_notify))
    return sid


@app.route("/transcription_callback/<number_to_notify>", methods=['POST'])
def transcription_callback(number_to_notify=None):
    print("received callback, number is: " + number_to_notify)
    log = key4me.fetch_transcript()
    message = "As of {}, the car is {}, speed is {} mph. "\
        + "http://www.google.com/maps/place/{:4f},{:4f}".format(
        log.call_time, log.car_status, log.speed, log.latitude, log.longitude)
    if number_to_notify is not None:
        n = phonenumbers.parse(number_to_notify, "US")
        if phonenumbers.is_valid_number(n):
            key4me.send_text(
                phonenumbers.format_number(n,
                                           phonenumbers.PhoneNumberFormat.E164),
                message)
    return "Ok"


@app.route("/fetch_transcript")
def fetch_transcript():
    log = key4me.fetch_transcript()
    print(text_format.MessageToString(log))
    return "http://www.google.com/maps/place/{:4f},{:4f}".format(
        log.latitude, log.longitude)


if __name__ == "__main__":
    app.run(debug=True)