from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.proxy_ips import ProxyIpsService
from app.schemas.proxy_ips import ProxyIpsIn
from app.utils.router_utils import create_response, handle_exceptions

proxy_ips_router = APIRouter(prefix="/proxy_ips", tags=["Proxy IPs"])


@proxy_ips_router.post("/add", response_model=dict)
async def add_proxy_ip(proxy_ip_data: ProxyIpsIn, request: Request):
    """新增代理IP"""
    session: AsyncSession = request.state.session
    try:
        proxy_ip = proxy_ip_data.proxy_ip
        # 检查是否已经存在
        if await ProxyIpsService.check_proxy_ip_exists(session, proxy_ip,proxy_ip_data.domain):
            raise HTTPException(status_code=400, detail="Proxy IP already exists")
        new_proxy_ip = await ProxyIpsService.add_proxy_ip(session, proxy_ip,proxy_ip_data.domain)
        return create_response(message="Proxy IP added successfully", data={"id": new_proxy_ip.id, "proxy_ip": proxy_ip})
    except Exception as e:
        return handle_exceptions(e)


@proxy_ips_router.get("/{proxy_ip}", response_model=dict)
async def check_proxy_ip(proxy_ip: str, request: Request):
    """检查代理IP是否存在"""
    session: AsyncSession = request.state.session
    try:
        exists = await ProxyIpsService.check_proxy_ip_exists(session, proxy_ip)
        if not exists:
            raise HTTPException(status_code=404, detail="Proxy IP not found")
        return create_response(message="Proxy IP exists", data={"proxy_ip": proxy_ip})
    except Exception as e:
        return handle_exceptions(e)
