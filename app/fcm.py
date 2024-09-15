import firebase_admin
from firebase_admin import credentials, messaging


def initialize_fcm():
    cred = credentials.Certificate(
        "/Users/kanghyojeong/Project/BalloonMap/balloon-map-net-firebase-adminsdk-5bxnq-58a37d54d4.json")
    firebase_admin.initialize_app(cred)


def send_notification(registration_token):
    message = messaging.Message(
        notification={
            "title": "BalloonMap",
            "body": "BalloonMap"
        },
        token=registration_token
    )

    response = messaging.send(message)
    print(response)
