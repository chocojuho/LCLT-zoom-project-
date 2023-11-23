import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['path'][6:-1]
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user.left',
                'username': self.scope["user"].username
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        receive_dict= json.loads(text_data)
        #print(text_data)
        message = receive_dict['message']
        action = receive_dict['action']
        if(action == 'new-offer') or (action == 'new-answer'):
            receiver_channel_name = receive_dict['message']['receiver_channel_name']
            receive_dict['message']['receiver_channel_name'] = self.channel_name
            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type' : 'send.sdp',
                    'receive_dict' : receive_dict
                }
            )
            return
        if action == 'out-peer':
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'send.sdp',
                'receive_dict' : receive_dict
            }
            )
            return
        receive_dict['message']['receiver_channel_name'] = self.channel_name
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'send.sdp',
                'receive_dict' : receive_dict
            }
        )
    
    async def send_sdp(self,event):
        receive_dict = event['receive_dict']
        await self.send(text_data = json.dumps(receive_dict))
        
    async def user_left(self, event):
        username = event['username']

        message = {
            'action': 'out-peer',
            'peer' : username,
            'message': {
                # Add other data you want to send about the user who left
            }
        }

        # Broadcast the user left message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'receive_dict': message
            }
        )
        
        