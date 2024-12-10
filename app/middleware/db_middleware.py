from fastapi.requests import Request
from app.models import AsyncSessionFactory
async def create_session(request:Request ,call_next):
    session = AsyncSessionFactory()
    request.state.session = session
    response = await call_next(request)
    await session.close()
    return response