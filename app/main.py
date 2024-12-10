import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.db_middleware import create_session
from app.routers.device import device_router
from app.routers.friend_url_domain import friend_url_domain_router
from app.routers.proxy_ips import proxy_ips_router

app=FastAPI()

app.add_middleware(BaseHTTPMiddleware,dispatch=create_session)
app.include_router(proxy_ips_router,prefix="/api")
app.include_router(device_router, prefix='/api')
app.include_router(friend_url_domain_router, prefix='/api')

@app.get('/')
async def root():
    return {'message': 'Hello World'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)