import pytest
from unittest.mock import Mock
from fastapi import WebSocket

from services.connections import ConnectionManager


@pytest.fixture
def manager():
    return ConnectionManager()

@pytest.fixture
def websocket_mock():
    return Mock(spec=WebSocket)

@pytest.mark.asyncio
async def test_connect(manager, websocket_mock):
    project_id = "123"
    await manager.connect(websocket_mock, project_id)
    assert project_id in manager.active_connections
    assert websocket_mock in manager.active_connections[project_id]

@pytest.mark.asyncio
async def test_disconnect(manager, websocket_mock):
    project_id = "123"
    await manager.connect(websocket_mock, project_id)
    await manager.disconnect(websocket_mock, project_id)
    assert project_id not in manager.active_connections

@pytest.mark.asyncio
async def test_send_message_no_connection(manager, websocket_mock):
    project_id = "123"
    message = "Hello, world!"
    with pytest.raises(RuntimeError):
        await manager.send_message(project_id, message)

@pytest.mark.asyncio
async def test_send_message_no_connection(manager, websocket_mock):
    project_id = "123"
    message = "Hello, world!"
    with pytest.raises(RuntimeError):
        await manager.send_message(project_id, message)

@pytest.mark.asyncio
async def test_disconnect_empty_project(manager, websocket_mock):
    project_id = "123"
    with pytest.raises(ValueError):
        await manager.disconnect(websocket_mock, project_id)



