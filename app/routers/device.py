from fastapi import APIRouter, Request
from fastapi import WebSocket, WebSocketDisconnect

from app.schemas.device import DeviceIn
from app.service.device import DeviceService
from app.utils.router_utils import create_response, handle_exceptions

device_router = APIRouter(prefix="/device", tags=["device"])


online_device = {}

@device_router.post('/add')
async def add_device(device: DeviceIn, request: Request):
    session = request.state.session
    try:
        await DeviceService.add_device(session=session, device=device)
        return create_response(message='设备添加成功')
    except Exception as e:
        return handle_exceptions(e)


@device_router.get('/all')
async def get_devices(request: Request):
    session = request.state.session
    try:
        devices = await DeviceService.get_all_devices(session=session)
        devices = [device.dict() for device in devices]
        return create_response(data=devices, message='查询成功')
    except Exception as e:
        return handle_exceptions(e)


@device_router.get('/{device_id}')
async def get_device_by_device_id(device_id: str, request: Request):
    session = request.state.session
    try:
        result = await DeviceService.get_device_by_device_id(session=session, device_id=device_id)
        return create_response(data=result, message='查询成功')
    except Exception as e:
        return handle_exceptions(e)


@device_router.delete('/delete')
async def delete_device(request: Request, device_id: str):
    session = request.state.session
    try:
        await DeviceService.delete_device(session=session, device_id=device_id)
        return create_response(message='设备已删除')
    except Exception as e:
        return handle_exceptions(e)


@device_router.put('/update/device_name')
async def update_device_name(request: Request, device: DeviceIn):
    session = request.state.session
    try:
        await DeviceService.update_device_name(session=session, device=device)
        return create_response(message='设备名称更改成功')
    except Exception as e:
        return handle_exceptions(e)


@device_router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'heartbeat':
                online_device.update({data.get('device_id'): websocket})
    except WebSocketDisconnect:
        disconnected_device_id = None
        for device_id, ws in online_device.items():
            if ws == websocket:
                disconnected_device_id = device_id
                break
        if disconnected_device_id:
            del online_device[disconnected_device_id]
