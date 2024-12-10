from fastapi import APIRouter, Request

from app.routers.device import online_device
from app.schemas.task import TaskIn, ExecuteTask
from app.service.device import DeviceService
from app.service.task import TaskService
from app.utils.router_utils import create_response, handle_exceptions

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post('/add')
async def add_task(request: Request, task_in: TaskIn):
    session = request.state.session
    try:
        await TaskService.add_task(session, task_in)
        return create_response(message='添加成功')
    except Exception as e:
        return handle_exceptions(e)


@task_router.delete('/delete')
async def delete_task(request: Request, task_in: TaskIn):
    session = request.state.session
    try:
        await TaskService.delete_task(session, task_in)
        return create_response(message='删除成功')
    except Exception as e:
        return handle_exceptions(e)


@task_router.put('/update')
async def update_task(request: Request, task_in: TaskIn):
    session = request.state.session
    try:
        await TaskService.update_task(session, task_in)
        return create_response(message='更新成功')
    except Exception as e:
        return handle_exceptions(e)


@task_router.get('/all')
async def all_tasks(request: Request):
    session = request.state.session
    try:
        result = await TaskService.get_all_tasks(session)
        return create_response(data=result)
    except Exception as e:
        return handle_exceptions(e)


@task_router.get('/{task_id}')
async def get_task(request: Request, task_id: str):
    session = request.state.session
    try:
        result = await TaskService.get_task_by_task_id(session, task_id)
        return create_response(data=result, message='查询成功')
    except Exception as e:
        return handle_exceptions(e)


@task_router.post('/execute_task')
async def execute_task(task: ExecuteTask):
    """
    在页面上选择一个任务，点击执行时，使用post方法发送到服务器，服务器发送到客户端
    :param task:
    :return:
    """
    try:
        await TaskService.execute_task(online_device=online_device, payload=task)
        return create_response(message='命令发送成功')
    except Exception as e:
        return handle_exceptions(e)


@task_router.get('/stop_task')
async def stop_task(task: ExecuteTask):
    try:
        await TaskService.stop_task(online_device=online_device, payload=task)
        return create_response(message='命令发送成功')
    except Exception as e:
        return handle_exceptions(e)
