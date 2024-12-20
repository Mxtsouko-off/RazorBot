import aiohttp
import asyncio
import json
import os
from datetime import datetime
from functions.Generator import GenAccesToken


class Status():
    @staticmethod
    async def run():
        info_api = f'http://lightswitch-public-service-prod.ol.epicgames.com/lightswitch/api/service/bulk/status?serviceId=Fortnite'
        
        access_token = await GenAccesToken.run()  
        if not access_token:
            print("Failed to retrieve access token. Exiting.")
            return
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept-Language": "en"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(info_api, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print("Data received successfully")
                else:
                    print(f"Failed to retrieve data. Status code: {response.status}")         
                            
            
            current_date = datetime.now().strftime('%d-%m')
            file_path = os.path.join(f'./data/{current_date}-RazorStatus.json')

            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                print(f'Saved modified mission file: {file_path}')
            except Exception as e:
                print(f"Error saving file: {e}")
                    
                    
                    
                    
        
