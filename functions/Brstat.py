import requests

class Brstat:
    @staticmethod
    def stat(name, platform):
        api = 'https://fortnite-api.com/v2/stats/br/v2'
        
        params = {
            'name': name,
            'accountType': platform
        }
        
        headers = {
            'Authorization': '8e0d9c96-05ab-4e44-b7d6-9a7b21113cc8'
        }
        
        response = requests.get(api, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f"Error {response.status_code}: {response.text}"}
