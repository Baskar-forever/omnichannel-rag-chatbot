from app.models.lead import Lead


class LeadRepository:

    def create(
        self,
        db,
        name: str,
        email: str,
        phone: str,
        enquiry: str = None,
        source: str = None
    ):

        lead = Lead(
            name=name,
            email=email,
            phone=phone,
            enquiry=enquiry,
            source=source
        )

        db.add(lead)

        db.commit()

        db.refresh(lead)

        return lead

    def get_by_id(
        self,
        db,
        lead_id: int
    ):

        return (
            db.query(Lead)
            .filter(
                Lead.id == lead_id
            )
            .first()
        )