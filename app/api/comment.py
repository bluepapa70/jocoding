"""
성과보고 승인 코멘트 생성 API - Anthropic API 프록시 엔드포인트.
"""
import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["comment"])

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"


class CommentRequest(BaseModel):
    prompt: str


@router.post("/generate-comment")
async def generate_comment(req: CommentRequest):
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="서버에 ANTHROPIC_API_KEY가 설정되지 않았습니다.")

    async with httpx.AsyncClient(timeout=60.0) as client:
        res = await client.post(
            ANTHROPIC_API_URL,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": req.prompt}],
            },
        )

    if not res.is_success:
        detail = res.json().get("error", {}).get("message", f"HTTP {res.status_code}")
        raise HTTPException(status_code=res.status_code, detail=detail)

    text = res.json().get("content", [{}])[0].get("text", "")
    if not text:
        raise HTTPException(status_code=500, detail="응답이 비어 있습니다.")

    return {"text": text.strip()}
