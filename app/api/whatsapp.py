from fastapi import (
APIRouter,
Request
)

from app.core.container import (
container
)

from app.db.database import (
SessionLocal
)

from app.services.whatsapp_service import (
send_text_message
)

from app.repositories.whatsapp_message_repository import (
WhatsAppMessageRepository
)


import json

router = APIRouter()

@router.post("/whatsapp/webhook")
async def receive_webhook(request: Request):


    body = await request.body()
    repository = (
    WhatsAppMessageRepository()
    )

    if not body:

        print(
            "Empty webhook body"
        )

        return {
            "status": "ok"
        }

    try:

        data = json.loads(
            body
        )

        print(
            "=" * 100
        )
        print(
            "FULL WEBHOOK PAYLOAD"
        )
        print(
            json.dumps(
                data,
                indent=2
            )
        )
        print(
            "=" * 100
        )

        value = (
            data["entry"][0]
            ["changes"][0]
            ["value"]
        )

        #
        # Ignore status updates
        #
        if "messages" not in value:

            print(
                "IGNORED: STATUS EVENT"
            )

            return {
                "status": "ok"
            }

        message = (
            value["messages"][0]
        )

        #
        # Ignore non-text messages
        #
        if (
            message.get("type")
            != "text"
        ):

            print(
                "IGNORED: NON TEXT MESSAGE"
            )

            return {
                "status": "ok"
            }

        sender = (
            message["from"]
        )

        text = (
            message["text"]["body"]
        )

        message_id = (
            message["id"]
        )

        print(
            f"SENDER: {sender}"
        )

        print(
            f"MESSAGE ID: {message_id}"
        )

        print(
            f"TEXT: {text}"
        )

        db = SessionLocal()

        if repository.exists(
        db,
        message_id
        ):

            
            print(
                f"Duplicate message ignored: {message_id}"
            )

            db.close()

            return {
                "status":
                "duplicate"
            }



        try:

            result = (
                container
                .whatsapp_service
                .process_message(
                    db=db,
                    phone_number=sender,
                    message=text
                )
            )

            print(
                "BOT RESPONSE:"
            )

            print(
                result
            )

            send_text_message(
                phone_number=sender,
                text=result["reply"]
            )

            repository.create(
                db,
                message_id
            )

        finally:

            db.close()

        return {
            "status": "ok"
        }

    except Exception as e:

        print(
            f"WhatsApp webhook error: {e}"
        )

        import traceback

        traceback.print_exc()

        return {
            "status": "error"
        }

