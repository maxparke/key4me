from yattag import Doc, indent
from key4me_pb2 import LocationLog

GOOGLE_MAPS_API_KEY = "AIzaSyBach1FZqujPT7pcTn9R24NeY2V-5N2orE"


def make_page(log):
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            with tag('title'):
                text('key4me')
        with tag('body'):
            line('h1', 'key4me')
            with tag('div', id="description"):
                text('key4me is a tool to find the ')
                with tag('a', href="https://key4all.com"):
                    text('key4all')
                text(
                    ' car.  This is entirely unofficial and unaffiliated with MSCHF.'
                )
            with tag('div', id="location"):
                text("As of {}, the car is {}, speed is {} mph. ".format(
                    log.call_time.ToJsonString(),
                    LocationLog.CarStatus.Name(log.car_status).lower(),
                    log.speed))
            doc.stag(
                'iframe',
                width="450",
                height="250",
                frameborder="0",
                style="border:0",
                referrerpolicy="no-referrer-when-downgrade",
                src=
                "https://www.google.com/maps/embed/v1/place?key={}&q={:4f},{:4f}"
                .format(GOOGLE_MAPS_API_KEY, log.latitude, log.longitude),
                allowfullscreen=True)

    return indent(doc.getvalue())
