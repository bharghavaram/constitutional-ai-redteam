"""Constitutional AI Red-Teaming Suite – FastAPI Application Entry Point."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.redteam import router as redteam_router
from app.core.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s – %(message)s")

app = FastAPI(
    title="Constitutional AI Red-Teaming Suite",
    description="Automated adversarial testing framework for LLM safety evaluation. Includes jailbreak detection, prompt injection testing, bias auditing, and constitutional AI compliance scoring based on OWASP LLM Top 10.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(redteam_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "service": "Constitutional AI Red-Teaming Suite",
        "version": "1.0.0",
        "docs": "/docs",
        "attack_categories": ["prompt_injection", "jailbreak", "data_extraction", "bias_probing", "hallucination_induction"],
        "capabilities": [
            "Iterative jailbreak attack generation (Tree of Attacks)",
            "Static attack library (OWASP LLM Top 10)",
            "Constitutional AI compliance scoring",
            "Bias auditing across demographic dimensions",
            "Risk level classification (CRITICAL/HIGH/MEDIUM/LOW)",
            "Judge-LLM safety evaluation",
        ],
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
