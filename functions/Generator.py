import aiohttp

class GenAccesToken():
    @staticmethod
    async def run():
        SWITCH_TOKEN = "OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"basic {SWITCH_TOKEN}",
            }
            data = {
                "grant_type": "client_credentials",
            }

            async with session.post(
                url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
                headers=headers,
                data=data
            ) as response:
                if response.status == 200:
                    token_data = await response.json()
                    return token_data.get("access_token")
                else:
                    print(f"Failed to generate access token: {response.status}")
                    error_data = await response.text()
                    print(error_data)
                    return None