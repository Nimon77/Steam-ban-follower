import discord, logging, steam, os
from dotenv import load_dotenv
from steam.steamid import SteamID
from steam.webapi import WebAPI
from discord import app_commands
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.cheater import Cheater, Base

load_dotenv()

token = os.environ.get('DISCORD_BOT_TOKEN')
steam_api = WebAPI(os.environ.get('STEAM_API_KEY'))

logger = logging.getLogger('discord')

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user} (ID: {client.user.id})')
    logger.info('------')

@client.tree.command(name='ping')
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message('Pong!', ephemeral=True)

@client.tree.command(name="add_cheater", description="Add a potential cheater to the database")
async def add_potential_cheater(interaction: discord.Interaction, *, urls_profile: str) -> None:
    session = Session()
    validUsers = []
    for url in urls_profile.split(' '):
        if (steamIdUser := steam.steamid.from_url(url)) is None:
            continue
        if (session.query(Cheater).filter_by(id_steam=steamIdUser.as_64).first()) is not None:
            continue
        validUsers.append(steamIdUser)
    if len(validUsers) == 0:
        await interaction.response.send_message("Users already un databases or invalid URLs", ephemeral=True)
        return
    logger.info(f"Adding {len(validUsers)} users to database")
    logger.debug(f"Users: {validUsers}")
    steamUsersInfo = steam_api.ISteamUser.GetPlayerSummaries(steamids=[user.as_64 for user in validUsers])['response']['players']
    steamUsersBans = steam_api.ISteamUser.GetPlayerBans(steamids=[user.as_64 for user in validUsers])['players']
    for steamUserInfo, steamUserBans in zip(steamUsersInfo, steamUsersBans):
        cheater = Cheater(
            added_by=interaction.user.id,
            steamId=steamUserInfo['steamid'],
            name=steamUserInfo['personaname'],
            nbr_VAC=steamUserBans['NumberOfVACBans'],
            nbr_game_bans=steamUserBans['NumberOfGameBans'],
            nbr_community_bans=steamUserBans['NumberOfGameBans'],
            days_since_last_ban=steamUserBans['DaysSinceLastBan']
        )
        session.add(cheater)
        session.commit()
    # steamUserInfo = steam_api.ISteamUser.GetPlayerSummaries(steamids=steamIdUser.as_64)['response']['players'][0]
    # steamUserBans = steam_api.ISteamUser.GetPlayerBans(steamids=steamIdUser.as_64)['players'][0]
    # cheater = Cheater(
    #     added_by=interaction.user.id,
    #     steamId=steamIdUser.as_64,
    #     name=steamUserInfo['personaname'],
    #     nbr_VAC=steamUserBans['NumberOfVACBans'],
    #     nbr_game_bans=steamUserBans['NumberOfGameBans'],
    #     nbr_community_bans=steamUserBans['NumberOfGameBans'],
    #     days_since_last_ban=steamUserBans['DaysSinceLastBan']
    # )
    # session.add(cheater)
    # session.commit()
    # await interaction.response.send_message(f"User `{steamUserInfo['personaname']}` added to the database")

if __name__ == '__main__':
    # set up sqlalchemy
    engine = create_engine('sqlite:///dev.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    # print all cheaters
    session = Session()
    for cheater in session.query(Cheater).all():
        print(cheater)

    client.run(token, log_level=logging.DEBUG)
    # client.run(os.environ['DISCORD_BOT_TOKEN'])
