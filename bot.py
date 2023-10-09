import discord
from os import system as sys
from paste import upload
from json import loads as dictconvert
from bottoken import token

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.attachments == []:
        return
    if message.attachments[0].filename.endswith('.txt') or message.attachments[0].filename.endswith('.log'):
        sys(f'echo message with log found from {message.author}')
        sys(f'curl -o log.txt {message.attachments[0].url} > /dev/null')
        pasteoutput = dictconvert(upload(message.author))
        link = pasteoutput['link']
        sys('rm log.txt')
        print("log saved to ", link)
        await message.reply(f'Looks like you sent a log without uploading it to a paste site <a:badrat:1152755787286982739> so I took the trouble of doing it for you: \n## [click here](<{link}>)\nPlease use `?paste` in <#664874942407507978> to see a link of sites you can use to post logs, so we don\'t have to download them')


client.run(token())