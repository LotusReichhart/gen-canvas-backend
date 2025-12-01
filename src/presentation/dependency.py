from fastapi import Request, Header

def get_lang(accept_language: str = Header(default="vi", convert_underscores=False)) -> str:
    return accept_language.split(",")[0].split("-")[0]

def get_current_user_id(request: Request) -> int:
    user_payload = getattr(request.state, "user", {})
    return int(user_payload.get("id", 0))

def get_current_user_payload(request: Request) -> dict:
    return getattr(request.state, "user", {})