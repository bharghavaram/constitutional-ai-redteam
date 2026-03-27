"""Constitutional AI Red-Teaming – API routes."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from app.services.redteam_service import RedTeamService, get_redteam_service, ATTACK_CATEGORIES

router = APIRouter(prefix="/redteam", tags=["Red-Teaming"])

class JailbreakRequest(BaseModel):
    goal: str
    attack_type: str = "jailbreak"
    max_iterations: Optional[int] = None

class StaticAttackRequest(BaseModel):
    attack_category: Optional[str] = None

@router.post("/jailbreak")
async def jailbreak_test(req: JailbreakRequest, svc: RedTeamService = Depends(get_redteam_service)):
    if not req.goal.strip():
        raise HTTPException(400, "goal cannot be empty")
    valid_types = list(ATTACK_CATEGORIES.keys())
    if req.attack_type not in valid_types:
        raise HTTPException(400, f"attack_type must be one of {valid_types}")
    return svc.run_jailbreak_test(req.goal, req.attack_type, req.max_iterations)

@router.post("/static-attacks")
async def static_attacks(req: StaticAttackRequest, svc: RedTeamService = Depends(get_redteam_service)):
    if req.attack_category and req.attack_category not in ATTACK_CATEGORIES:
        raise HTTPException(400, f"Unknown category. Use: {list(ATTACK_CATEGORIES.keys())}")
    return svc.run_static_attacks(req.attack_category)

@router.post("/bias-audit")
async def bias_audit(svc: RedTeamService = Depends(get_redteam_service)):
    return svc.run_bias_audit()

@router.get("/results")
async def get_results(svc: RedTeamService = Depends(get_redteam_service)):
    return {"results": svc.get_results()}

@router.get("/attack-categories")
async def attack_categories():
    return {"categories": list(ATTACK_CATEGORIES.keys())}

@router.get("/health")
async def health():
    return {"status": "ok", "service": "Constitutional AI Red-Teaming Suite"}
