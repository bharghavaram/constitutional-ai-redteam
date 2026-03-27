"""Tests for Constitutional AI Red-Teaming Suite."""
import pytest
from unittest.mock import MagicMock, patch
from app.core.config import settings
from app.services.redteam_service import ATTACK_CATEGORIES, SAFETY_CONSTITUTION


def test_settings():
    assert settings.MAX_ATTACK_ITERATIONS == 5
    assert settings.JAILBREAK_THRESHOLD == 0.7
    assert settings.TEMPERATURE == 0.9


def test_attack_categories_exist():
    required = ["prompt_injection", "jailbreak", "data_extraction", "bias_probing", "hallucination_induction"]
    for cat in required:
        assert cat in ATTACK_CATEGORIES
        assert len(ATTACK_CATEGORIES[cat]) > 0


def test_safety_constitution_completeness():
    assert len(SAFETY_CONSTITUTION) >= 6
    for principle in SAFETY_CONSTITUTION:
        assert len(principle) > 10


def test_risk_classification():
    risk_mapping = {
        (True, 0.9): "CRITICAL",
        (False, 0.7): "HIGH",
        (False, 0.4): "MEDIUM",
        (False, 0.1): "LOW",
    }
    for (jailbreak, score), expected_risk in risk_mapping.items():
        risk = "CRITICAL" if jailbreak else (
            "HIGH" if score > 0.6 else (
                "MEDIUM" if score > 0.3 else "LOW"
            )
        )
        assert risk == expected_risk


def test_attack_prompts_have_placeholders():
    for cat in ["prompt_injection", "jailbreak"]:
        for prompt in ATTACK_CATEGORIES[cat]:
            assert "{malicious_goal}" in prompt, f"Missing placeholder in: {prompt}"


@pytest.mark.asyncio
async def test_api_health():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    resp = client.get("/api/v1/redteam/health")
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_api_attack_categories():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    resp = client.get("/api/v1/redteam/attack-categories")
    assert resp.status_code == 200
    data = resp.json()
    assert "categories" in data
    assert len(data["categories"]) == 5


@pytest.mark.asyncio
async def test_api_jailbreak_invalid_type():
    from fastapi.testclient import TestClient
    from main import app
    client = TestClient(app)
    resp = client.post("/api/v1/redteam/jailbreak", json={"goal": "test", "attack_type": "invalid"})
    assert resp.status_code == 400
