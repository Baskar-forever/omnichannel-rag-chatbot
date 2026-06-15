from app.db.database import SessionLocal

from app.repositories.session_repository import (
    SessionRepository
)

from app.repositories.lead_repository import (
    LeadRepository
)

from app.repositories.message_repository import (
    MessageRepository
)


def main():

    db = SessionLocal()

    session_repo = SessionRepository()
    lead_repo = LeadRepository()
    message_repo = MessageRepository()

    try:

        print("\n" + "=" * 80)
        print("CREATE SESSION")
        print("=" * 80)

        session = session_repo.create(db)

        print(f"Session ID: {session.id}")
        print(f"State: {session.state}")
        print(f"Pending Data: {session.pending_data}")

        print("\n" + "=" * 80)
        print("UPDATE STATE")
        print("=" * 80)

        session = session_repo.update_state(
            db=db,
            session=session,
            state="ASK_EMAIL"
        )

        print(f"State: {session.state}")

        print("\n" + "=" * 80)
        print("UPDATE PENDING DATA")
        print("=" * 80)

        pending_data = {
            "name": "Baskar"
        }

        session = session_repo.update_pending_data(
            db=db,
            session=session,
            pending_data=pending_data
        )

        print(session.pending_data)

        print("\n" + "=" * 80)
        print("CREATE LEAD")
        print("=" * 80)

        lead = lead_repo.create(
            db=db,
            name="Baskar",
            email="baskar@gmail.com",
            phone="9876543210",
            source="website"
        )

        print(f"Lead ID: {lead.id}")
        print(f"Name: {lead.name}")

        print("\n" + "=" * 80)
        print("ATTACH LEAD TO SESSION")
        print("=" * 80)

        session = session_repo.attach_lead(
            db=db,
            session=session,
            lead_id=lead.id
        )

        print(
            f"Session Lead ID: {session.lead_id}"
        )

        print("\n" + "=" * 80)
        print("SAVE USER MESSAGE")
        print("=" * 80)

        user_message = message_repo.create(
            db=db,
            session_id=session.id,
            role="user",
            content="What cloud services do you provide?"
        )

        print(
            f"Message ID: {user_message.id}"
        )

        print("\n" + "=" * 80)
        print("SAVE ASSISTANT MESSAGE")
        print("=" * 80)

        assistant_message = message_repo.create(
            db=db,
            session_id=session.id,
            role="assistant",
            content="We provide cloud migration and DevOps services."
        )

        print(
            f"Message ID: {assistant_message.id}"
        )

        print("\n" + "=" * 80)
        print("GET SESSION MESSAGES")
        print("=" * 80)

        messages = message_repo.get_by_session(
            db=db,
            session_id=session.id
        )

        for message in messages:

            print(
                f"[{message.role}] "
                f"{message.content}"
            )

        print("\n" + "=" * 80)
        print("ALL TESTS PASSED")
        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()