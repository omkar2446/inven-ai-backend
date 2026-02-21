from backend.models.agent_suggestion import AgentSuggestion
from backend.models import db

def create_notification(product_id,stype,desc):

    sug=AgentSuggestion(
        product_id=product_id,
        suggestion_type=stype,
        description=desc
    )

    db.session.add(sug)
    db.session.commit()