from dataclasses import dataclass
from datetime import datetime

from ..domain.entities.claim import Claim
from ..domain.entities.item import Item


@dataclass
class ItemSummaryDTO:
    id: str
    report_type: str
    title: str
    description_public: str
    category: str
    location_text: str
    happened_at: datetime
    status: str


@dataclass
class ItemDetailDTO(ItemSummaryDTO):
    pass


@dataclass
class ManagedItemDetailDTO(ItemDetailDTO):
    posted_by_user_id: int
    verification_questions: list[str]
    active_claim_id: str | None


@dataclass
class ClaimReviewDTO:
    id: str
    item_id: str
    claimant_user_id: int
    answers: list[str]
    status: str
    submitted_at: datetime


@dataclass
class ClaimQuestionsDTO:
    item_id: str
    questions: list[str]


@dataclass
class AuditLogDTO:
    id: int
    actor_user_id: int
    action: str
    target_type: str
    target_id: str
    created_at: datetime


def to_item_summary_dto(item: Item) -> ItemSummaryDTO:
    return ItemSummaryDTO(
        id=str(item.id),
        report_type=item.report_type.value,
        title=item.title,
        description_public=item.description_public,
        category=item.category,
        location_text=item.location_text,
        happened_at=item.happened_at,
        status=item.status.value,
    )


def to_item_detail_dto(item: Item) -> ItemDetailDTO:
    return ItemDetailDTO(
        **to_item_summary_dto(item).__dict__,
    )


def to_managed_item_detail_dto(item: Item) -> ManagedItemDetailDTO:
    return ManagedItemDetailDTO(
        **to_item_detail_dto(item).__dict__,
        posted_by_user_id=item.posted_by_user_id,
        verification_questions=[
            question.question
            for question in item.verification_questions
        ],
        active_claim_id=str(item.active_claim_id) if item.active_claim_id else None,
    )


def to_claim_review_dto(claim: Claim) -> ClaimReviewDTO:
    return ClaimReviewDTO(
        id=str(claim.id),
        item_id=str(claim.item_id),
        claimant_user_id=claim.claimant_user_id,
        answers=claim.answers,
        status=claim.status.value,
        submitted_at=claim.submitted_at,
    )


def to_claim_questions_dto(item: Item) -> ClaimQuestionsDTO:
    return ClaimQuestionsDTO(
        item_id=str(item.id),
        questions=[question.question for question in item.verification_questions],
    )


def to_audit_log_dto(model) -> AuditLogDTO:
    return AuditLogDTO(
        id=model.id,
        actor_user_id=model.actor_user_id,
        action=model.action,
        target_type=model.target_type,
        target_id=model.target_id,
        created_at=model.created_at,
    )
