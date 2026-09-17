from fastapi import APIRouter
from app.core.verification import FixVerificationEngine
from app.schemas.fix import VerifyFixRequest, VerifyFixResponse

router = APIRouter(tags=["Verification"])

@router.post("/verify", response_model=VerifyFixResponse)
def verify_fix(req: VerifyFixRequest):
    return FixVerificationEngine.verify_patch(
        original_code=req.original_code,
        patched_code=req.patched_code,
        language=req.language or "python",
        rule_id=req.rule_id
    )
