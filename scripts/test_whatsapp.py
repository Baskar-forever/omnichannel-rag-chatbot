import requests

WHATSAPP_ACCESS_TOKEN = ""

WHATSAPP_PHONE_ID = ""

WHATSAPP_API_URL = ""



def send_text_message(
    phone_number,
    text
):

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
        "STATUS:",
        response.status_code
    )

    print(
        response.text
    )


send_text_message(
    "919344410204",
    "Hello from ZenFuture"
)