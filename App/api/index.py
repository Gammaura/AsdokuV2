import os
import sys

# Tambahkan root direktori ke sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import app

# Middleware penyesuai route untuk Vercel Serverless
class VercelPathMiddleware:
    def __init__(self, asgi_app):
        self.asgi_app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            for prefix in ["/api/index.py", "/api/index", "/api"]:
                if path == prefix:
                    scope["path"] = "/"
                    break
                elif path.startswith(prefix + "/"):
                    # Pengecualian: jangan strip jika route memang berawalan /api/ (seperti /api/format)
                    if prefix == "/api" and any(path.startswith(r) for r in ["/api/format", "/api/download", "/api/active-learning"]):
                        break
                    scope["path"] = path[len(prefix):]
                    break
        await self.asgi_app(scope, receive, send)

app.add_middleware(VercelPathMiddleware)
