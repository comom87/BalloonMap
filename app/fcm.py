import firebase_admin
from firebase_admin import credentials, messaging


def initialize_fcm():
    cred = credentials.Certificate(
        "/home/ubuntu/BalloonMap/balloon-map-net-firebase-adminsdk-5bxnq-58a37d54d4.json")
    firebase_admin.initialize_app(cred)


def send_notification(registration_token):
    print(f"send_notification: {registration_token}")
    message = messaging.Message(
        notification=messaging.Notification(
            title="BalloonMap",
            body="주변 30m 내에서 오물 풍선이 감지되었습니다."
        ),
        token=registration_token
    )

    response = messaging.send(message)
    print(response)
