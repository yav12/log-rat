import discord
from discord import app_commands
from os import system as sys
from paste import upload
from json import loads as dictconvert
from tokens import token
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

@client.event
async def on_ready():
    await tree.sync()
    print(f'We have logged in as {client.user}')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.attachments == []:
        return
    link_list = []
    logfound = False
    for attachment in message.attachments:
        if attachment.filename.endswith('.txt') or attachment.filename.endswith('.log'):
            logfound = True;
            sys(f'echo message with log found from {message.author}')
            log = requests.get(attachment.url, allow_redirects=True)
            with open('log.txt', "w") as f: f.write(log.text)
            response = upload(message.author)
            pasteoutput = dictconvert(response)
            link = pasteoutput['link']
            sys('rm log.txt')
            print("log saved to ", link)
            link_list.append(link)
    if logfound:
        logbuttons = log_buttons(link_list)
        for role in message.author.roles:
            # helper, creator, dev team
            if role.id == 658488705123614731 or role.id == 760900030051123242 or role.id == 897971533098655784:
                await message.reply("Here you go:", view=logbuttons)
                return
        
        await message.reply('Looks like you sent a log without uploading it to a paste site <a:badrat:1152755787286982739> so I took the trouble of doing it for you. Please use `?paste` in <#664874942407507978> to see a link of sites you can use to post logs, so we don\'t have to download them', view=logbuttons)
        

@tree.command(name="upload", description="Upload a log to paste.ee")
@app_commands.describe(file='The log to be uploaded')
async def slash_command(interaction: discord.Interaction, 
                        file: discord.Attachment):  
    if file.filename.endswith('.txt') or file.filename.endswith('.log'):
        sys(f'echo upload command used by {interaction.user.name}')
        log = requests.get(file.url, allow_redirects=True)
        with open('log.txt', "w") as f: f.write(log.text)
        response = upload(interaction.user.name)
        pasteoutput = dictconvert(response)
        link = pasteoutput['link']
        sys('rm log.txt')
        print("log saved to ", link)
        await interaction.response.send_message(f"Log uploaded to {link}")
        
def log_buttons(links):
    buttonlist = Buttons()
    for i in range(len(links)):
        buttonlist.add_item(discord.ui.Button(label=f"Link to log {i + 1}", style=discord.ButtonStyle.link, url=links[i],emoji="<a:SCLAUNDRY2:853888948098564126>"))
    return buttonlist
        

def print_links(links):
    logs = ["## "]
    for i in range(len(links)):
        realnumber = i + 1
        logs.append(f"[Log {str(realnumber)}](<{links[i]}>) ")
    return ''.join(logs)


token = token()
client.run(token)
