import requests
import aiohttp
from functions.AccountID import Get_Account_ID
                
class DBLookup():
    @staticmethod
    async def search(epic):
        print('executed (DBLookup)')
        url = 'https://fortnitedb.com/profile/'
        AccountID1 = await Get_Account_ID.op(epic)
        
        if AccountID1:
            print('Executed (GetAccountID)')
            link = f'{url}/{AccountID1}'
            print(link)
            
            return link
        else:
            return 'Oops! We Encountered An Error, (This account does not exist or has a private profile)!'
            
        
        
        
