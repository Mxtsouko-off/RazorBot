import requests
from functions.Generator import GenAccesToken
import json
import os
from datetime import datetime

class MissionDev():
    @staticmethod
    async def run():
        access_token = await GenAccesToken.run()  
        if not access_token:
            print("Failed to retrieve access token. Exiting.")
            return
        
        info_url = "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/world/info"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept-Language": "en"
        }
        
        response = requests.get(info_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("Data received successfully")
            
            def replace_mission_alert_guid(data):
                if isinstance(data, dict):
                    for key, value in data.items():
                        if key == "missionAlertGuid":
                            data[key] = ""
                        else:
                            replace_mission_alert_guid(value)
                elif isinstance(data, list):
                    for item in data:
                        replace_mission_alert_guid(item)

            replace_mission_alert_guid(data)
            
            current_date = datetime.now().strftime('%d-%m')
            file_path = os.path.join(f'{current_date}-RazorMissionDev.json')

            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                print(f'Saved modified mission file: {file_path}')
            except Exception as e:
                print(f"Error saving file: {e}")
        else:
            print(f'Failed to get world info: {response.status_code}')
            print(response.text)
