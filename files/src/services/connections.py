from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, project_id: str):
        await websocket.accept()
        if project_id not in self.active_connections:
            self.active_connections[project_id] = []
        self.active_connections[project_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, project_id: str):
        if project_id in self.active_connections:
            self.active_connections[project_id].remove(websocket)
            if not self.active_connections[project_id]:
                del self.active_connections[project_id]
        else:
            raise ValueError(f"No active connections for project ID {project_id}")

    async def send_message(self, project_id: str, message: str):
        if project_id not in self.active_connections or not self.active_connections[project_id]:
            raise RuntimeError(f"No active connections for project ID {project_id}")

        await self.active_connections[project_id][0].send_text(message)

manager = ConnectionManager()