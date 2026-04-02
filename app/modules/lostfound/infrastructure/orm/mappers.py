from uuid import UUID

from ...domain.entities.claim import Claim
from ...domain.entities.item import Item, VerificationQuestion
from ...domain.value_objects.claim_status import ClaimStatus
from ...domain.value_objects.item_status import ItemStatus
from ...domain.value_objects.report_type import ReportType
from .models import ClaimModel, ItemModel


def map_item_model_to_domain(model: ItemModel) -> Item:
    return Item(
        id=UUID(model.id),
        report_type=ReportType(model.report_type),
        title=model.title,
        description_public=model.description_public,
        category=model.category,
        location_text=model.location_text,
        happened_at=model.happened_at,
        posted_by_user_id=model.posted_by_user_id,
        status=ItemStatus(model.status),
        verification_questions=[
            VerificationQuestion(question.question)
            for question in model.verification_questions
        ],
        active_claim_id=UUID(model.active_claim_id) if model.active_claim_id else None,
    )


def map_claim_model_to_domain(model: ClaimModel) -> Claim:
    return Claim(
        id=UUID(model.id),
        item_id=UUID(model.item_id),
        claimant_user_id=model.claimant_user_id,
        answers=[answer.answer for answer in model.answers],
        status=ClaimStatus(model.status),
        submitted_at=model.submitted_at,
    )
