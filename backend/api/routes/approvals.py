from fastapi import APIRouter, HTTPException

from backend.core.demo_runtime import runtime
from backend.database.schemas import ApprovalDecision

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.get("")
async def list_approvals():
    return runtime.get_approvals()


@router.post("/{approval_id}/decision")
async def submit_decision(approval_id: str, decision: ApprovalDecision):
    try:
        return await runtime.respond_to_approval(
            approval_id,
            decision.decision,
            comment=decision.comment,
            edited_content=decision.edited_content,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Approval not found: {exc.args[0]}") from exc