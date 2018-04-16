import discord
import requests
import configparser
import os
import psutil

config = configparser.ConfigParser()
config.read('settings.ini')
token = config['settings']['token']
client = discord.AutoShardedClient()

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='quack !duck | https://random-d.uk'))
    print('Ducky has started')

@client.event
async def on_message(message):
    if message.content.lower() == '!duck':
        r = requests.get('https://api.random-d.uk/random')
        answer = r.json()
        em = discord.Embed(title='A random duck just for you!')
        em.set_image(url=answer['url'])
        em.set_footer(text=answer['message'])
        await message.channel.send(embed=em)
    if message.content.lower().startswith('!getduck'):
        number = message.content.replace('!getduck ','')
        em = discord.Embed(title='Here\'s the duck you wanted!')
        em.set_image(url='https://api.random-d.uk/images/{}.jpg'.format(number))
        em.set_footer(text='Powered by random-d.uk')
        await message.channel.send(embed=em)
    if message.content.lower() == '!help':
        em = discord.Embed(title='Ducky Help',description='**!duck**: Gives you a random duck\n**!getduck** [number]: Gives you a specific duck\n**!help**: Shows this message')
        em.set_author(name=str(client.user), icon_url=client.user.avatar_url)
        r = requests.get('https://api.random-d.uk/random')
        answer = r.json()
        em.set_thumbnail(url=answer['url'])
        em.set_footer(text='random-d.uk duck bot')
        await message.channel.send(embed=em)
    if message.content.lower() == '!info':
        em = discord.Embed(title='About Ducky')
        r = requests.get('https://api.random-d.uk/random')
        answer = r.json()
        process = psutil.Process(os.getpid())
        em.set_thumbnail(url=answer['url'])
        em.set_author(name=str(client.user), icon_url=client.user.avatar_url)
        em.add_field(name='Library',value='discord.py rewrite 1.0.0a', inline=True)
        em.add_field(name='Version', value='Python 3.5.2', inline=True)
        em.add_field(name='Website', value='https://random-d.uk')
        em.add_field(name='Memory Usage',value=str(round(process.memory_info()[0]/1000000,0)) + ' MB')
        em.add_field(name='CPU Usage', value=str(process.cpu_percent(0.1)) + '%')
        em.set_footer(text='Made by Auxim#0001')
        await message.channel.send(embed=em)

client.run(token)
