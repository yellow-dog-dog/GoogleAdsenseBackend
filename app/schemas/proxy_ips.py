from pydantic import BaseModel


class ProxyIpsIn(BaseModel):
    proxy_ip: str
    domain: str


class ProxyIpsOut(BaseModel):
    proxy_ip: str
