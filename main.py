import discord, os, discord.ext, mysql.connector
from discord.ext import commands
from discord.ext.commands import has_permissions
from dotenv import load_dotenv

load_dotenv()

SQL_USERNAME = os.environ['SQL_USERNAME']
SQL_PASSWORD = os.environ['SQL_PASSWORD']
SQL_SERVER = os.environ['SQL_SERVER']
SQL_PORT = os.environ['SQL_PORT']

SQL = mysql.connector.connect(
  host=SQL_SERVER,
  user=SQL_USERNAME,
  password=SQL_PASSWORD,
  database=SQL_USERNAME
)

cursor = SQL.cursor()

client = discord.Client()

client = commands.Bot(command_prefix = "c.")

async def getServers():
  cursor.execute("SELECT * FROM `main`")
  r = cursor.fetchall()
  d = {}
  for item in r:
    d[item[0]] = item[1]
  return d

@client.event
async def on_ready():
  activity = discord.Activity(type=discord.ActivityType.watching, name="for c.help")
  await client.change_presence(activity=activity)
  print("Bot Online")


@client.event
async def on_message(message):
  if not message.content.startswith("c."):
    set = await getServers()
    if str(message.guild.id) in set:
      send = set[str(message.guild.id)] == str(message.channel.id)
    else:
      send = False
    if not message.author.id == 951564560077320262 and send:
      attachments = message.attachments
      files = []
      for attachment in attachments:
        file = await attachment.to_file()
        files.append(file)
      for server in set:
        if not server == str(message.guild.id):
          guild = client.get_guild(int(server))
          if guild:
            channels = guild.text_channels
            for channel in channels:
              if set[str(guild.id)] == str(channel.id):
                messages = []
                async for m in channel.history(limit=100):
                  messages.append(m)
                removeStart=False
                for mes in messages:
                  if mes.author.id == 951564560077320262 and mes.content.startswith(f"**{message.author}** from **{message.guild}**"):
                    removeStart = True

                if removeStart:
                  await channel.send(f"{message.content}",files=files)
                else:
                  await channel.send(f"**{message.author}** from **{message.guild}**\n{message.content}",files=files)
  await client.process_commands(message)


client.remove_command('help')
@client.command(name="help",aliases=["?"])
async def help(ctx):
  await ctx.reply("Use c.set to set the channel")


@client.command(name="set")
@has_permissions(manage_messages=True)
async def setChannel(ctx,channel:discord.TextChannel=None):
  if not channel:
    channel = ctx.channel
  try:
    cursor.execute(f"INSERT INTO `main` (`server_id`, `channel_id`) VALUES ('{ctx.guild.id}', '{ctx.channel.id}')")
  except mysql.connector.errors.IntegrityError:
    cursor.execute(f"UPDATE `main` SET `channel_id` = '{ctx.channel.id}' WHERE `main`.`server_id` = '{ctx.guild.id}'")
  SQL.commit()
  await ctx.reply(f"Set channel to {channel.mention}")

token = os.environ["token"]
client.run(token)
# invite link - https://discord.com/oauth2/authorize?client_id=951564560077320262&permissions=116736&scope=bot