import disnake
from disnake.ext import commands, tasks
import aiohttp
import time
import requests
import asyncio
import json
from datetime import datetime, timedelta, time
import re
import flask
from flask import Flask, jsonify, request
from threading import Thread
from io import BytesIO
import os
from functions.AccountID import Get_Account_ID
from functions.FortniteShop import FortniteShop
from functions.Generator import GenAccesToken
from functions.Brstat import Brstat
from functions.Dumper import DumperFile
from functions.MissionsDev import MissionDev
from functions.Status import Status
from functions.DBFinder import DBLookup
import random

Missions = os.getenv("MissionID")

NEWS_API = {
    "news": "https://fortnite-api.com/v2/news",
    "brnews": "https://fortnite-api.com/v2/news/br",
    "stwnews": "https://fortnite-api.com/v2/news/stw",
    "creativenew": "https://fortnite-api.com/v2/news/creative"
}

HEADER = {
    'language': 'fr'
}

def fetch_news(news_type):
    url = NEWS_API.get(news_type)
    if not url:
        return {'error': "Invalid news type."}

    response = requests.get(url, headers=HEADER)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Error {response.status_code}: {response.text}"}
    
    
def time_until_next_1am():
    now = datetime.now()
    next_run = datetime.combine(now.date(), time(1, 0)) 
    if now >= next_run:  
        next_run += timedelta(days=1)
    return (next_run - now).total_seconds()

@tasks.loop(hours=24) 
async def daily_task():
    current_date = datetime.now().strftime('%d-%m')
    file_name = f"{current_date}-RazorMissionDev.json"
    file_path = os.path.join(os.getcwd(), file_name)
    channel = bot.get_channel(1319581165153161226)

    if channel is None:
        print("Channel not found. Please check the channel ID.")
        return

    if not os.path.exists(file_path):
        load_file = await MissionDev.run()

        if not load_file:
            print("An error occurred while generating the file.")
            return

        if not os.path.exists(file_path):
            print("File was not created even though MissionDev.run() succeeded.")
            return

    try:
        embed = disnake.Embed(
            title="`🏔️` ***Razor/MissionDev***",
            description="Here you can download the daily missions file.",
            color=disnake.Color.blue(),
        )
        embed.set_thumbnail(
            url="https://stw-planner.com/images/Heroes/Ninja/T-Ninja-HID-Ninja-028-Razor-SR-T01-L.png"
        )

        with open(file_path, "rb") as f:
            file = disnake.File(f, filename=file_name)
            await channel.send(embed=embed, file=file)

        await asyncio.sleep(30)
        os.remove(file_path)
        print(f"File {file_name} deleted successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

@daily_task.before_loop
async def before_daily_task():
    await bot.wait_until_ready()

    wait_time = time_until_next_1am()
    print(f"Waiting {wait_time / 60:.2f} minutes until the next 1 AM task execution.")
    await asyncio.sleep(wait_time) 

    print("First execution after bot restart.")
    await daily_task()  
                
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(
    command_prefix='+',
    intents=disnake.Intents.all(),
    help_command=None,
    test_guilds=[1304168745845129297],  
    command_sync_flags=command_sync_flags,
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    daily_task.start()
    
@tasks.loop(seconds=3)
async def statut():
    activity_list = ["https://dsc.gg/stwboost", "➕!RazorPrem", "!By Mxtsouko 🎈"]
    selected = random.choice(activity_list)
    status_list = [disnake.Status.idle, disnake.Status.do_not_disturb, disnake.Status.online]
    selected_status = random.choice(status_list)

    await bot.change_presence(
        status=selected_status,
        activity=disnake.Activity(
            type=disnake.ActivityType.streaming,
            name=selected,
            url='https://www.twitch.tv/mxtsouko'
        )
    )


@bot.slash_command(name='getid', description="Get account ID using display name")
async def getid(ctx, epic: str):
    displayname = epic
    account_id = await Get_Account_ID.op(displayname)
    
    em = disnake.Embed(
        title=f'Display: {displayname}',
        description=f'```{account_id}```',
        color=disnake.Color.dark_orange()
    )
    em.set_thumbnail(url='https://stw-planner.com/images/Heroes/Ninja/T-Ninja-HID-Ninja-028-Razor-SR-T01-L.png')
    await ctx.send(embed=em)
    
@bot.slash_command(name='shopfile', description="show fortnite shop file")
async def shop(ctx):
    shop_items = await FortniteShop.get_shop_items()

    if isinstance(shop_items, dict):
        em = disnake.Embed(
            title="Here is today's Fortnite shop file",
            description="You can download the file containing the complete list of items in the store.",
            color=disnake.Color.dark_orange()
        )
        em.set_thumbnail(url='https://stw-planner.com/images/Heroes/Ninja/T-Ninja-HID-Ninja-028-Razor-SR-T01-L.png')

        with open('fortnite_shop.json', 'rb') as f:
            file = disnake.File(f, filename=f"{ctx.author}-RazorFnShop.json")
            await ctx.send(embed=em, file=file, ephemeral=True)
            
        time.sleep(30)
        os.remove('fortnite_shop.json')

    else:
        await ctx.send(content=f'{KeyError}', ephemeral=True)
        await ctx.send(shop_items, ephemeral=True)
        
        
@bot.slash_command(name='missiondev', description='Get daily mission file')
@commands.has_role('➕!RazorPrem')
async def missiondev(ctx: disnake.ApplicationCommandInteraction):
    await ctx.response.defer(ephemeral=True)

    try:
        current_date = datetime.now().strftime('%d-%m')
        file_name = f"{current_date}-RazorMissionDev.json"
        file_path = os.path.join(os.getcwd(), file_name)

        if not os.path.exists(file_path):
            load_file = await MissionDev.run()

            print(f"MissionDev.run() result: {load_file}")

            if not load_file:
                await ctx.edit_original_message(content="An error occurred while generating the file.")
                asyncio.sleep(5)
                embed = disnake.Embed(
                    title='`🏔️` ***Razor/MissionDev***',
                    description='Here you can download your missions file.',
                    color=disnake.Color.blue()
                )
                embed.set_thumbnail(url='https://stw-planner.com/images/Heroes/Ninja/T-Ninja-HID-Ninja-028-Razor-SR-T01-L.png')

                with open(file_path, 'rb') as f:
                    file = disnake.File(f, filename=f"{ctx.author}-RazorMissionDev.json")
                    await ctx.edit_original_message(content='thanks you for using', embed=embed, file=file)

                await asyncio.sleep(30)
                os.remove(file_path)
                print(f"File {file_name} deleted successfully.")
                return

            if not os.path.exists(file_path):
                print("File was not created even though MissionDev.run() succeeded.")
                await ctx.edit_original_message(content="An error occurred while generating the file.")
                return

        embed = disnake.Embed(
            title='`🏔️` ***Razor/MissionDev***',
            description='Here you can download your mission file.',
            color=disnake.Color.blue()
        )
        embed.set_thumbnail(url='https://stw-planner.com/images/Heroes/Ninja/T-Ninja-HID-Ninja-028-Razor-SR-T01-L.png')

        with open(file_path, 'rb') as f:
            file = disnake.File(f, filename=f"{ctx.author}-RazorMissionDev.json")
            await ctx.edit_original_message(embed=embed, file=file)

        await asyncio.sleep(30)
        os.remove(file_path)
        print(f"File {file_name} deleted successfully.")

    except PermissionError:
        await ctx.edit_original_message(
            content="You don't have permission to use this command. It is reserved for Razor Premium members."
        )
    except FileNotFoundError:
        await ctx.edit_original_message(
            content="An error occurred: The mission file could not be found or was already deleted."
        )
    except Exception as e:
        await ctx.edit_original_message(content=f"An unexpected error occurred: {str(e)}")
        
@bot.slash_command(name='fnstatus', description='Get fortnite status')
@commands.has_role('➕!RazorPrem')
async def fnstatus(ctx: disnake.ApplicationCommandInteraction):
    await ctx.response.defer(ephemeral=True)

    try:
        current_date = datetime.now().strftime('%d-%m')
        file_name = f"data/{current_date}-RazorStatus.json"
        file_path = os.path.join(os.getcwd(), file_name)

        if not os.path.exists(file_path):
            load_file = await Status.run()

            print(f"Status.run() result: {load_file}")

            if not load_file:
                await ctx.edit_original_message(content="An error occurred while generating the file.")
                await asyncio.sleep(5)
                embed = disnake.Embed(
                        title='`🌴` ***Razor/StatusFile***',
                        description='Here you can download your status file.',
                        color=disnake.Color.blue()
                    )
                embed.set_thumbnail(url='https://stw-planner.com/images/Heroes/Ninja/T-Ninja-HID-Ninja-028-Razor-SR-T01-L.png')

                with open(file_path, 'rb') as f:
                    file = disnake.File(f, filename=f"{ctx.author}-RazorStatus.json")
                    await ctx.edit_original_message(content='thanks you for using', embed=embed, file=file)

                await asyncio.sleep(30)
                os.remove(file_path)
                print(f"File {file_name} deleted successfully.")
                return

        if not os.path.exists(file_path):
            print("File was not created even though Status.run() succeeded.")
            await ctx.edit_original_message(content="An error occurred while generating the file.")
            return

        embed = disnake.Embed(
                title='`🌴` ***Razor/StatusFile***',
                description='Here you can download your status file.',
                color=disnake.Color.blue()
            )
        embed.set_thumbnail(url='https://stw-planner.com/images/Heroes/Ninja/T-Ninja-HID-Ninja-028-Razor-SR-T01-L.png')

        with open(file_path, 'rb') as f:
            file = disnake.File(f, filename=f"{ctx.author}-RazorStatus.json")
            await ctx.edit_original_message(embed=embed, file=file)

        await asyncio.sleep(30)
        os.remove(file_path)
        print(f"File {file_name} deleted successfully.")

    except PermissionError:
        await ctx.edit_original_message(
            content="You don't have permission to use this command. It is reserved for Razor Premium members."
        )
    except FileNotFoundError:
        await ctx.edit_original_message(
            content="An error occurred: The mission file could not be found or was already deleted."
        )
    except Exception as e:
        await ctx.edit_original_message(content=f"An unexpected error occurred: {str(e)}")
        
        
@bot.slash_command(description="Retrieve Fortnite player statistics.")
async def brstat(
    inter: disnake.ApplicationCommandInteraction, 
    username: str, 
    platform: str = commands.Param(choices=["epic", "psn", "xbl"])
):
    """
    Slash command to fetch Fortnite statistics.
    
    Parameters:
    - inter : Interaction of the command.
    - username : Player's username.
    - platform : Platform (epic, psn, xbl).
    """
    await inter.response.defer(ephemeral=True) 

    result = Brstat.stat(username, platform)

    if 'error' in result:
        await inter.followup.send(result['error'], ephemeral=True)
    else:
        stats = result.get('data', {}).get('stats', {})
        if not stats:
            await inter.followup.send("No statistics found for this player.", ephemeral=True)
        else:
            overall = stats.get('all', {}).get('overall', {})
            wins = overall.get('wins', 'N/A')
            kills = overall.get('kills', 'N/A')
            matches = overall.get('matches', 'N/A')
            kd_ratio = overall.get('kd', 'N/A')
            lastModified = overall.get('lastModified', 'N/A')
            death = overall.get('deaths', 'N/A')
            

            embed = disnake.Embed(
                title=f"Fortnite Stats: {username}",
                description=f"Platform: {platform}",
                color=disnake.Color.dark_orange()
            )
            embed.add_field(name="Wins", value=wins, inline=True)
            embed.add_field(name="Eliminations", value=kills, inline=True)
            embed.add_field(name="Kill", value=matches, inline=True)
            embed.add_field(name="K/D Ratio", value=kd_ratio, inline=True)
            embed.add_field(name="Death", value=death, inline=True)
            embed.add_field(name="LastModified", value=lastModified, inline=True)

            embed.set_footer(text="RazorVerse !")

            await inter.followup.send(embed=embed, ephemeral=True)

@bot.slash_command(description="Retrieve Fortnite news.")
async def news(
    inter: disnake.ApplicationCommandInteraction,
    news_type: str = commands.Param(choices=["news", "brnews", "stwnews", "creativenew"])
):
    """
    Command to fetch Fortnite news based on the chosen category.

    Parameters:
    - inter: Interaction object for the command.
    - news_type: Type of news (news, brnews, stwnews, creativenew).
    """
    await inter.response.defer(ephemeral=True)  
    
    result = fetch_news(news_type)

    if 'error' in result:
        await inter.followup.send(result['error'], ephemeral=True)
    else:
        if news_type == "news":
            news_data = result.get("data", {}).get("br", {}).get("motds", [])
        elif news_type == "stwnews":
            news_data = result.get("data", {}).get("messages", [])
        else:
            news_data = result.get("data", {}).get("motds", [])

        if not news_data:
            await inter.followup.send("No news available for this category.", ephemeral=True)
        else:
            embeds = []
            for item in news_data[:5]: 
                title = item.get("title", "No Title")
                body = item.get("body", "No Description")
                image_url = item.get("image", None)

                embed = disnake.Embed(
                    title=title,
                    description=body,
                    color=disnake.Color.green()
                )
                if image_url:
                    embed.set_image(url=image_url)

                embed.set_footer(text=f"Source: Fortnite {news_type}", icon_url="https://fortnite-api.com/favicon.ico")
                embeds.append(embed)

            await inter.followup.send(embeds=embeds, ephemeral=True)
            

@bot.slash_command(name='map', description='Get the Fortnite map with POI locations')
async def map(ctx: disnake.ApplicationCommandInteraction):
    url = "https://fortnite-api.com/v1/map"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        map_image = data["data"]["images"]["blank"]
        pois = data["data"]["pois"]
        
        embed = disnake.Embed(
            title="Fortnite Map",
            description="Here is the current Fortnite map with POI locations.",
            color=disnake.Color.blue()
        )
        embed.set_image(url=map_image)
        
        poi_list = "\n".join([f"{poi['name']} - Coordinates: {poi['location']['x']}, {poi['location']['y']}, {poi['location']['z']}" for poi in pois])
        
        if len(poi_list) > 1024:
            poi_list = poi_list[:1020] + "..."  
        
        embed.add_field(name="Points of Interest (POIs)", value=poi_list, inline=False)
        
        await ctx.send(embed=embed)
    else:
        await ctx.send("Failed to retrieve the Fortnite map data. Please try again later.")

@bot.slash_command(description="edit your missions file to funny_file")
@commands.has_role('➕!RazorPrem')
async def dumper(inter: disnake.ApplicationCommandInteraction, file: disnake.Attachment):
    await inter.response.defer(ephemeral=True)

    if not file.filename.endswith(".json"):
        await inter.edit_original_message(content="Please provide a valid JSON file.")
        return

    try:
        file_content = await file.read()

        updated_data = DumperFile.process_file(file_content)

        output_file_path = f"{inter.author}-RazorDevMission.json"
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            json.dump(updated_data, output_file, ensure_ascii=False, indent=2)

        await inter.edit_original_message(content="Your file has been successfully edited. :")
        await inter.followup.send(file=disnake.File(output_file_path), ephemeral=True)
        os.remove(output_file_path)

    except json.JSONDecodeError:
        await inter.edit_original_message(content="The file sent is not a valid JSON file.")
    except Exception as e:
        await inter.edit_original_message(content=f"An error occurred while processing: {e}")
        
@bot.slash_command(description='find player in fortnitedb')
async def dbfinder(ctx, epic:str):
    linkdb = await DBLookup(epic)
    em = disnake.Embed(title='***/RazorVerse/DBFinder*** 🔎', description=f'click on the boutton or: {linkdb}', color=disnake.Color.green())
    class DBLINK(disnake.ui.Button):
            def __init__(self):
                super().__init__(label=f"click to open player: {epic} in FortniteDB", style=disnake.ButtonStyle.link, url=f"{linkdb}")
                

    view = disnake.ui.View()
    view.add_item(DBLINK())
    await ctx.send(embed=em, view=view, ephemeral=True)

    
@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = disnake.Embed(title="`📍`Oh No", description=f"An unexpected error occurred `📍`",
                              color=disnake.Color.brand_red())
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        pass


app = Flask('')

@app.route('/')
def main():
    return f"Logged in as {bot.user}."

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()


bot.run(os.getenv('TOKEN'))
