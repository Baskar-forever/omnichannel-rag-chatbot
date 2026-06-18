import os
import requests

from dotenv import load_dotenv

load_dotenv()

class WhatsAppService:


    def __init__(
            self,
            chat_service,
            session_repository
        ):

            self.chat_service = (
                chat_service
            )

            self.session_repository = (
                session_repository
            )

    def process_message(
            self,
            db,
            phone_number: str,
            message: str
        ):

            session = (
                self.session_repository
                .get_by_phone_number(
                    db,
                    phone_number
                )
            )

            if not session:

                session = (
                    self.session_repository
                    .create_whatsapp_session(
                        db,
                        phone_number
                    )
                )

                return {
                    "reply":
                        "Welcome to ZenFuture Technologies. "
                        "May I know your name?"
                }

            return (
                self.chat_service
                .process_message(
                    db=db,
                    session_id=session.id,
                    message=message
                )
            )


WHATSAPP_ACCESS_TOKEN = (
os.getenv(
"WHATSAPP_ACCESS_TOKEN"
)
)

WHATSAPP_PHONE_ID = (
os.getenv(
"WHATSAPP_PHONE_ID"
)
)

WHATSAPP_API_URL = (
"https://graph.facebook.com/v23.0"
)

def send_text_message(
    phone_number,
    text
    ):


    try:

        url = (
            f"{WHATSAPP_API_URL}/"
            f"{WHATSAPP_PHONE_ID}/messages"
        )

        headers = {
            "Authorization":
                f"Bearer {WHATSAPP_ACCESS_TOKEN}",

            "Content-Type":
                "application/json"
        }

        payload = {
            "messaging_product":
                "whatsapp",

            "to":
                phone_number,

            "type":
                "text",

            "text": {
                "body":
                    text
            }
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        print(
            "WhatsApp Status:",
            response.status_code
        )

        print(
            response.text
        )

        return response.ok

    except Exception as e:

        print(
            f"WhatsApp Send Error: {e}"
        )

        return False

