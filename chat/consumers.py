import json
from channels.generic.websocket import AsyncWebsocketConsumer
import urllib.parse  # Import URL decoder


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_name = urllib.parse.unquote(self.room_name).replace(" ", "_")[:100]  # Sanitize room name
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        sender = data['sender']
        file_data = data.get('file_data', None)  # Base64 file content
        file_name = data.get('file_name', None)  # Filename

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'file_data': file_data,
                'file_name': file_name
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'file_data': event['file_data'],  # Forward file data
            'file_name': event['file_name']
        }))
