from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from services.connections import manager


router = APIRouter(prefix="/websocket")


@router.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    await manager.connect(websocket, project_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(project_id, f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)
