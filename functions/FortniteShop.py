import aiohttp
import json

class FortniteShop():
    @staticmethod
    async def get_shop_items():
        SHOP_API_URL = "https://fortniteapi.io/v2/shop?lang=fr&includeRenderData=true&includeHiddenTabs=true"
        
        headers = {
            "Authorization": "fb2a07a9-847e7658-3ca6c699-7d42c202",
            "accept": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(SHOP_API_URL, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    with open('fortnite_shop.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    return data
                else:
                    return f"Erreur lors de la récupération de la boutique : {response.status}"