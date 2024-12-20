import aiohttp

class Get_Account_ID():
    @staticmethod
    async def op(displayname):
        url = f"https://fortniteapi.io/v2/lookup/advanced?username={displayname}"
        headers = {
            "Authorization": "fb2a07a9-847e7658-3ca6c699-7d42c202",
            "accept": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('result') and len(data['matches']) > 0:
                        account_id = data['matches'][0]['accountId']
                        return account_id
                    else:
                        return f"Aucun compte trouvé pour '{displayname}'."
                else:
                    return f"Erreur {response.status}: Impossible de récupérer l'ID pour {displayname}."