import asyncio
import json
import os
import websockets


class SocketClient:
    
    @staticmethod
    def send_message(data):
        """Клиент для отправки сообщений через сокет"""
        SKK_SOCKET = os.environ.get("SKK_SOCKET")
        
        async def _send():
            async with websockets.connect(SKK_SOCKET) as ws:
                await ws.send(json.dumps(data))
                response = await ws.recv()
                return json.loads(response)
        
        return asyncio.run(_send())