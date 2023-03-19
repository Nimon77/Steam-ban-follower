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
        if (session.query(Cheater).filter_by(steamId=steamIdUser.as_64).first()) is not None:
            continue
        validUsers.append(steamIdUser)
    if len(validUsers) == 0:
        await interaction.response.send_message("Users already un databases or invalid URLs", ephemeral=True)
        return
    logger.info(f"Adding {len(validUsers)} users to database")
    logger.debug(f"Users: {validUsers}")

    for i in range(0, len(validUsers), 100):
        listIds = [str(user.as_64) for user in validUsers[i:i+100]]
        steamUsersInfo = steam_api.ISteamUser.GetPlayerSummaries(steamids=','.join(listIds))['response']['players']
        steamUsersBans = steam_api.ISteamUser.GetPlayerBans(steamids=','.join(listIds))['players']
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
    await interaction.response.send_message(f"Added {len(validUsers)} users to database", ephemeral=False)

@client.tree.command(name="check_all_cheaters", description="Check all cheaters in the database")
async def check_all_cheaters(interaction: discord.Interaction) -> None:
    session = Session()
    cheaters = session.query(Cheater).all()
    if len(cheaters) == 0:
        await interaction.response.send_message("No cheaters in database", ephemeral=True)
        return
    logger.info(f"Checking {len(cheaters)} users in database")
    logger.debug(f"Users: {cheaters}")
    for i in range(0, len(cheaters), 100):
        listIds = [str(cheater.steamId) for cheater in cheaters[i:i+100]]
        steamUsersBans = steam_api.ISteamUser.GetPlayerBans(steamids=','.join(listIds))['players']
        for cheater, steamUserBans in zip(cheaters[i:i+100], steamUsersBans):
            await interaction.channel.send(f"Checking `{cheater.name}`")
            cheater.nbr_VAC = steamUserBans['NumberOfVACBans']
            cheater.nbr_game_bans = steamUserBans['NumberOfGameBans']
            cheater.nbr_community_bans = steamUserBans['NumberOfGameBans']
            cheater.days_since_last_ban = steamUserBans['DaysSinceLastBan']
            session.commit()
    await interaction.response.send_message(f"Done", ephemeral=False)

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
