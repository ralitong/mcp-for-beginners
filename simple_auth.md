Creating a server with Authentication
```python
app = FastMCP(
    name="MCP Resource Server",
    instructions="Resource Server that validates tokens via Authorization Server instropection",
    host=settings["host"],
    port=settings["port"],
    debug=True
)

# creating starlette web app
starlette_app = app.streamable_http_app()

# serving app via uvicorn
async def run(starlette_app):
    import uvicorn
    config = uvicorn.Config(
        starlette_app,
        host=app.settings.host,
        port=app.settings.port,
        log_level=app.settings.log_level.lower(),
    )
    server = uvicorn.Server(config)
    await server.serve()
```

Authentication Middleware
```python
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        has_header = request.headers.get("Authorization")
        
        if not has_header:
            print("-> Missing Authorization header!")
            return Response(status_code=401, content="Unauthorized")
        
        if valid_token(has_header):
            print("-> Invalid token!")
            return Response(status_code=403, content="Forbidden")

        
        print("Valid token, proceeding...")

        respone = await call_next(request)
        # add any customer headers or change in the response in some way
        return response

    def valid_token(token: str) -> bool:
        # remove the "Bearer " prefix
        if.token.startswith("Bearer "):
            token = token[7:]
            return token == "secret-token"
        return False

starlette_app.add_middleware(CustomHeaderMiddleware)
```

JSON Web Token way of authenticating
```python
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime

# Secret key used to sign the JWT
secret_key = 'your-secret-key'

header = {
    "alg": "HS256",
    "typ": "JWT"
}

# the user info audit claims and expiry time
payload = {
    "sub": "1234567890",               # Subject (user ID)
    "name": "User Userson",            # Custom claim
    "admin": True,                     # Custom claim
    "iat": datetime.datetime.utcnow(), # Issued at
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiry
}

# encode it
encoded_jwt = jwt.encode(payload, secret_key, algorithm="HS256", headers=header)
```

Validation a JSON Web Token
```python
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        print("✅ Token is valid.")
        print("Decoded claims")
        for key, value in decoded.items():
            print(f"    {key}: {value}")
    except ExpiredSignatureError:
        print("❌ Token has expired.")
    except InvalidTokenError as e:
        print(f"❌ Invalid token: {e}")
```

Role Based Access Control
```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt

# DON'T have the secret in the code like this, this is for demonstration purposes only. Read it from a safe place
SECRET_KEY = "your-secret-key" # put this in env variable
REQUIRED_PERMISSION = "User.Read"

class JWTPermissionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse({"error": "Missing or invalid Authorization header", status_code=401})
        
        token = auth_header.split(" ")[1]

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JSONResponse({"error": "Token expired", status_code=401})
        except jwt.InvalidTokenError:
            return JSONResponse({"error": "Invalid token", status_code=401})
        
        permissions = decoded.get("permission", [])
        if REQUIRED_PERMISSION not in permissions:
            return JSONResponse({"error": "Permission denied", status_code=403})
        
        request.state.user = decoded
        return await call_next(request)
```

Integrating the middleware
```python
# Alt 1: add middleware while constructing starlette app
middleware = [
    MiddleWare(JWTPermissionMiddleWare)
]

app = Starlette(routes=routes, middleware=middleware)

# Alt 2: add middleware after starlette app is already constructed
starlette_app.add_middleware(JWTPermissionMiddleware)

# Alt 3: add middleware per route
routes = [
    Route(
        "/mcp",
        endpoint=..., # handler
        middleware=[Middleware(JWTPermissionMiddleware)]
    )
]
```

Add RBAC to MCP
```python
@tool
def delete_product(id: int):
    try:
        check_permissions(role="Admin.Write", request)
    catch:
        pass # client failed authorization, raise authorization error

```