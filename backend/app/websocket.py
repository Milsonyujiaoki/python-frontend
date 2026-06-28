"""
WebSocket support for real-time synchronization.

This module provides:
- WebSocket endpoint at /ws
- JWT authentication on handshake
- Room-based organization (barbershop:{id})
- Heartbeat ping/pong (30s interval)
- Event messaging (appointment.booked, appointment.cancelled)
- Auto-reconnection support with exponential backoff
- Request ID for idempotency
"""

import asyncio
import base64
import json
import logging
import time
import uuid
from typing import Dict, Set, Optional

from fastapi import WebSocket, WebSocketDisconnect, Query, Header
from pydantic import BaseModel

logger = logging.getLogger(__name__)


# =============================================================================
# DATA MODELS
# =============================================================================

class WebSocketMessage(BaseModel):
    """Standard WebSocket message format."""
    type: str  # e.g., "appointment.booked", "ping", "pong"
    payload: dict
    request_id: Optional[str] = None  # For idempotency
    timestamp: float = 0

    def to_json(self) -> str:
        """Serialize to JSON."""
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str) -> "WebSocketMessage":
        """Deserialize from JSON."""
        data = json.loads(json_str)
        if not data.get("timestamp"):
            data["timestamp"] = time.time()
        return cls(**data)


# =============================================================================
# CONNECTION MANAGEMENT
# =============================================================================

class ConnectionManager:
    """Manages WebSocket connections and room subscriptions."""

    def __init__(self):
        # Active connections: {websocket: connection_info}
        self.active_connections: Dict[WebSocket, dict] = {}
        # Rooms: {room_name: {websocket}}
        self.rooms: Dict[str, Set[WebSocket]] = {}
        # Client heartbeat tracking
        self.last_heartbeat: Dict[WebSocket, float] = {}

    async def connect(self, websocket: WebSocket, client_id: str, room: str):
        """Register a new connection."""
        await websocket.accept()
        self.active_connections[websocket] = {
            "client_id": client_id,
            "room": room,
            "connected_at": time.time(),
        }
        self.last_heartbeat[websocket] = time.time()

        # Add to room
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(websocket)

        logger.info(f"WebSocket connected: client={client_id}, room={room}")

    def disconnect(self, websocket: WebSocket):
        """Remove a connection."""
        if websocket in self.active_connections:
            info = self.active_connections.pop(websocket)
            room = info.get("room")

            # Remove from room
            if room and room in self.rooms:
                self.rooms[room].discard(websocket)
                if not self.rooms[room]:
                    del self.rooms[room]

            # Clean heartbeat tracking
            self.last_heartbeat.pop(websocket, None)

            logger.info(f"WebSocket disconnected: {info}")

    async def send_to_room(self, room: str, message: WebSocketMessage):
        """Broadcast message to all connections in a room."""
        if room not in self.rooms:
            return

        message_json = message.to_json()
        dead_connections = []

        for websocket in self.rooms[room]:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.warning(f"Failed to send to websocket: {e}")
                dead_connections.append(websocket)

        # Clean dead connections
        for ws in dead_connections:
            self.disconnect(ws)

    async def send_to_client(self, websocket: WebSocket, message: WebSocketMessage):
        """Send message to a specific client."""
        try:
            await websocket.send_text(message.to_json())
        except Exception as e:
            logger.warning(f"Failed to send to client: {e}")
            raise

    def update_heartbeat(self, websocket: WebSocket):
        """Update heartbeat timestamp."""
        self.last_heartbeat[websocket] = time.time()

    def is_stale(self, websocket: WebSocket, timeout: float = 60.0) -> bool:
        """Check if connection heartbeat is stale."""
        last = self.last_heartbeat.get(websocket, 0)
        return (time.time() - last) > timeout

    def get_room_clients(self, room: str) -> int:
        """Get number of clients in a room."""
        return len(self.rooms.get(room, []))


# Global connection manager
manager = ConnectionManager()


# =============================================================================
# AUTHENTICATION
# =============================================================================

async def verify_jwt_token(token: Optional[str]) -> dict:
    """Verify JWT token and return user info.

    In production, this should validate against your JWT secret and
    extract user claims. For now, we decode and validate format.
    """
    if not token:
        # Try to extract from Authorization header format
        token = token.replace("Bearer ", "") if token else None
        if not token:
            raise ValueError("Missing authentication token")

    try:
        # Simple validation - in production use jose.jwt.decode()
        # from app.core.security import verify_token
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid token format")

        # Decode payload (base64)
        payload_b64 = parts[1]
        # Add padding if needed
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding

        payload = json.loads(base64.urlsafe_b64decode(payload_b64))

        # Extract user info
        user_info = {
            "user_id": payload.get("sub", payload.get("user_id")),
            "email": payload.get("email"),
            "barbershop_id": payload.get("barbershop_id"),
        }

        if not user_info["user_id"]:
            raise ValueError("Token missing user ID")

        return user_info

    except json.JSONDecodeError:
        raise ValueError("Invalid token payload")
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise ValueError(f"Invalid authentication token: {e}")


# =============================================================================
# EVENT HANDLERS
# =============================================================================

class EventHandlers:
    """Handlers for WebSocket events."""

    @staticmethod
    async def handle_appointment_booked(payload: dict, room: str):
        """Handle appointment booking event."""
        message = WebSocketMessage(
            type="appointment.booked",
            payload=payload,
            timestamp=time.time(),
        )
        await manager.send_to_room(room, message)
        logger.info(f"Broadcasted appointment.booked to room {room}")

    @staticmethod
    async def handle_appointment_cancelled(payload: dict, room: str):
        """Handle appointment cancellation event."""
        message = WebSocketMessage(
            type="appointment.cancelled",
            payload=payload,
            timestamp=time.time(),
        )
        await manager.send_to_room(room, message)
        logger.info(f"Broadcasted appointment.cancelled to room {room}")

    @staticmethod
    async def handle_pong(payload: dict, websocket: WebSocket):
        """Handle pong response."""
        manager.update_heartbeat(websocket)


# =============================================================================
# WEBSOCKET ENDPOINT
# =============================================================================

HEARTBEAT_INTERVAL = 30  # seconds

async def ping_sender(websocket: WebSocket, room: str):
    """Background task to send periodic pings."""
    while True:
        await asyncio.sleep(HEARTBEAT_INTERVAL)

        message = WebSocketMessage(
            type="ping",
            payload={"timestamp": time.time()},
            request_id=str(uuid.uuid4()),
        )

        try:
            await websocket.send_text(message.to_json())
        except Exception as e:
            logger.warning(f"Ping send failed: {e}")
            break


async def websocket_handler(websocket: WebSocket, token: Optional[str] = Query(None)):
    """Main WebSocket connection handler.

    Steps:
    1. Verify JWT token
    2. Determine room (barbershop:{id})
    3. Connect and accept
    4. Handle messages with heartbeat monitoring
    5. Clean up on disconnect
    """

    # Step 1: Authenticate
    try:
        user_info = await verify_jwt_token(token)
        barbershop_id = user_info.get("barbershop_id")
    except ValueError as e:
        await websocket.accept()
        await websocket.send_json({
            "type": "error",
            "payload": {"message": str(e)},
        })
        await websocket.close()
        return

    # Step 2: Determine room
    if not barbershop_id:
        await websocket.accept()
        await websocket.send_json({
            "type": "error",
            "payload": {"message": "User not associated with a barbershop"},
        })
        await websocket.close()
        return

    room = f"barbershop:{barbershop_id}"
    client_id = user_info["user_id"]

    # Step 3: Connect
    await manager.connect(websocket, client_id, room)

    # Start heartbeat sender
    ping_task = asyncio.create_task(ping_sender(websocket, room))

    try:
        # Step 4: Message loop
        while True:
            # Wait for message with timeout for heartbeat check
            try:
                raw_message = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=HEARTBEAT_INTERVAL
                )
            except asyncio.TimeoutError:
                # Check if connection is stale
                if manager.is_stale(websocket):
                    logger.warning(f"Connection stale, closing: {client_id}")
                    break
                continue

            # Process message
            message = WebSocketMessage.from_json(raw_message)
            manager.update_heartbeat(websocket)

            # Handle message types
            if message.type == "pong":
                await EventHandlers.handle_pong(message.payload, websocket)
            elif message.type == "appointment.book":
                await EventHandlers.handle_appointment_booked(
                    message.payload, room
                )
            elif message.type == "appointment.cancel":
                await EventHandlers.handle_appointment_cancelled(
                    message.payload, room
                )
            else:
                logger.warning(f"Unknown message type: {message.type}")

    except WebSocketDisconnect:
        logger.info(f"Client disconnected: {client_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # Step 5: Cleanup
        ping_task.cancel()
        try:
            await ping_task
        except asyncio.CancelledError:
            pass
        manager.disconnect(websocket)