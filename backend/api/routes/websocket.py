from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.core.websocket_manager import ws_manager

router = APIRouter(tags=["Realtime"])


@router.websocket("/ws/{run_id}")
async def run_stream(websocket: WebSocket, run_id: str):
    await ws_manager.connect(websocket, run_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, run_id)
    except Exception:
        ws_manager.disconnect(websocket, run_id)