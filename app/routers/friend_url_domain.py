from fastapi import APIRouter, HTTPException, Request
from app.schemas.friend_url_domain import FriendUrlDomainIn, FriendUrlDomainOut
from app.service.friend_url_domain import FriendUrlDomainService
from app.utils.router_utils import create_response, handle_exceptions

friend_url_domain_router = APIRouter(prefix="/friend_url", tags=["Friend URL"])


@friend_url_domain_router.post("/", response_model=dict)
async def add_friend_url(domain_data: FriendUrlDomainIn, request: Request):
    """新增友链域名"""
    session = request.state.session
    try:
        new_entry = await FriendUrlDomainService.create_friend_url(session, domain_data.domain)
        return create_response(message="Domain added successfully", data={"domain_id": new_entry.id})
    except Exception as e:
        return handle_exceptions(e)


@friend_url_domain_router.get("/{domain}", response_model=dict)
async def get_friend_url(domain: str, request: Request):
    """根据域名查询记录"""
    session = request.state.session
    try:
        record = await FriendUrlDomainService.get_friend_url_by_domain(session, domain)
        if not record:
            raise HTTPException(status_code=404, detail="Domain not found")
        return create_response(
            data={"domain": record.domain, "create_time": record.create_time},
            message="Query successful"
        )
    except Exception as e:
        return handle_exceptions(e)


@friend_url_domain_router.delete("/{domain}", response_model=dict)
async def delete_friend_url(domain: str, request: Request):
    """根据域名删除记录"""
    session = request.state.session
    try:
        deleted_count = await FriendUrlDomainService.delete_friend_url_by_domain(session, domain)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Domain not found")
        return create_response(message="Domain deleted successfully", data={"domain": domain})
    except Exception as e:
        return handle_exceptions(e)


@friend_url_domain_router.get("/{domain}/count", response_model=dict)
async def count_friend_url_today(domain: str, request: Request):
    """统计域名今天的出现次数"""
    session = request.state.session
    try:
        count = await FriendUrlDomainService.count_domain_today(session, domain)
        return create_response(
            data={"domain": domain, "count_today": count},
            message="Count query successful"
        )
    except Exception as e:
        return handle_exceptions(e)
