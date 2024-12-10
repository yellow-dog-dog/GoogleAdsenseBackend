from fastapi import APIRouter, Request

from app.schemas.profile import ProfileIn
from app.service.profile import ProfileService
from app.utils.router_utils import create_response, handle_exceptions

profile_router = APIRouter(prefix="/profile", tags=["profile"])


@profile_router.post('/add')
async def add_profile(request: Request, profile_in: ProfileIn):
    session = request.state.session
    try:
        result = await ProfileService.add_profile(session, profile_in=profile_in)
        return create_response(data=result, message='添加成功')
    except Exception as e:
        return handle_exceptions(e)


@profile_router.delete('/delete')
async def delete_profile(request: Request, profile_in: ProfileIn):
    session = request.state.session
    try:
        await ProfileService.delete_profile_by_profile_id(session, profile_in.profile_id)
        return create_response(message='删除成功')
    except Exception as e:
        return handle_exceptions(e)


@profile_router.put('/update')
async def update_profile(request: Request, profile_in: ProfileIn):
    session = request.state.session
    try:
        await ProfileService.update_profile_by_profile_id(session, profile_in=profile_in)
        return create_response(message='更新成功')
    except Exception as e:
        return handle_exceptions(e)


@profile_router.get('/all')
async def all_profiles(request: Request):
    session = request.state.session
    try:
        result = await ProfileService.get_all_profiles(session)
        return create_response(data=result, message='查询成功')
    except Exception as e:
        return handle_exceptions(e)


@profile_router.get('/{profile_id}')
async def profile(request: Request, profile_id: str):
    session = request.state.session
    try:
        result = await ProfileService.get_profile_by_profile_id(session, profile_id)
        return create_response(data=result, message='查询成功')
    except Exception as e:
        return handle_exceptions(e)
