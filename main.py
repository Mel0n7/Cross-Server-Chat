import discord, os, discord.ext, json, requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

client = commands.Bot(command_prefix = "c.")

@client.event
async def on_ready():
  activity = discord.Activity(type=discord.ActivityType.watching, name="for c.help")
  await client.change_presence(activity=activity)
  print("Bot Online")


@client.event
async def on_message(ctx):
  if not ctx.author.id == 951564560077320262:
    print(f"msg in {ctx.guild.name}:{ctx.guild.id} thats says {ctx.content} by {ctx.author}")
    attachments = ctx.attachments
    files = []
    for attachment in attachments:
      file = await attachment.to_file()
      files.append(file)
    with open("./set.json","r") as setF:
      set = json.loads(setF.read())
      for server in set:
        if not server == str(ctx.guild.id):
          guild = client.get_guild(int(server))
          channels = guild.text_channels
          for channel in channels:
            if set[str(guild.id)] == str(channel.id):
              await channel.send(f"**{ctx.author}**\n{ctx.content}",files=files)


client.remove_command('help')
@client.command(name="help",aliases=["?"])
async def help(ctx):
  await ctx.reply("Use c.set to set the channel")


@client.command(name="set")
async def setChannel(ctx,channel:discord.TextChannel=None):
  if not channel:
    channel = ctx.channel
  with open("./set.json","r") as set:
    set = json.loads(set.read())
  with open("./set.json","w") as setw:
    set[str(ctx.guild.id)] = str(channel.id)
    json.dump(set,setw)
  await ctx.reply(f"Set channel to #{channel}")
  print(f"Set channel to #{channel}")



token = os.environ["token"]
client.run(token)
# invite link - https://discord.com/oauth2/authorize?client_id=951564560077320262&permissions=116736&scope=bot