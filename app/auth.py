import base64
import json
from pathlib import Path

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class BasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Load users from users.json
        users_file = Path(__file__).parent / "users.json"
        self.users = json.loads(users_file.read_text())

    async def dispatch(self, request, call_next):
        # 1. Get Authorization header
        auth_header = request.headers.get("Authorization")

        # 2. Check it exists and starts with "Basic "
        if not auth_header or not auth_header.startswith("Basic "):
            return Response(
                "Unauthorized",
                status_code=401,
                headers={"WWW-Authenticate": "Basic"}
            )
        
        # 3. Decode the base64 part (after "Basic ")
        try:
            encoded = auth_header[6:] # Skip "Basic "
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
        except Exception:
            return Response("Invalid credentials", status_code=401)
        
        # 4. Validate against users dict
        if self.users.get(username) != password:
            return Response("Invalid credentials", status_code=401)
        
        # 5. Success - continue to the actual requests
        return await call_next(request)
