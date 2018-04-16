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
        em = discord.Embed(title='Ducky Help',description='**!duck**: Gives you a random duck\n**!getduck** [number]: Gives you a specific duck\n**!info**: Gives you some info about the bot\n**!invite**: Invite this bot**!userinfo [mention]**: Information about a user\n**!serverinfo**: Information about the server the bot is on\n**!help**: Shows this message')
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
        em.add_field(name='Github', value='https://github.com/random-duk/discord-bot')
        em.set_footer(text='Made by Auxim#0001')
        await message.channel.send(embed=em)
    if message.content == '!invite':
        await message.channel.send('https://random-d.uk/invite')
    if message.content.lower().startswith('!userinfo'):
        member = message.mentions[0]
        roles = []
        for role in member.roles:
            if role.is_default():
                continue
            else:
                roles.append(role.mention)
        em = discord.Embed(title='Userinfo',color=member.color)
        em.set_author(name=str(member), icon_url=member.avatar_url)
        em.add_field(name='Joined at',value=str(member.joined_at.strftime('%a, %-d %b %Y at %H:%M:%S GMT')))
        em.add_field(name='Created at', value=str(member.created_at.strftime('%a, %-d %b %Y at %H:%M:%S GMT')))
        em.add_field(name='Roles [{}]'.format(len(roles)), value=' '.join(roles))
        em.add_field(name='Status',value=str(member.status))
        if member.id == member.guild.owner.id:
            em.add_field(name='Owner',value='Yes')
        if member.is_avatar_animated():
            em.add_field(name='Nitro',value='Yes')
        em.set_thumbnail(url=member.avatar_url)
        em.set_footer(text='ID: ' + str(member.id),icon_url=message.guild.icon_url)
        await message.channel.send(embed=em)
    if message.content.lower().startswith('!serverinfo'):
        em = discord.Embed(title='Serverinfo')
        em.set_author(name=str(message.guild), icon_url=message.guild.icon_url)
        em.set_thumbnail(url=message.guild.icon_url)
        em.add_field(name='Region',value=str(message.guild.region))
        em.add_field(name='Verification Level',value=str(message.guild.verification_level))
        em.add_field(name='Owner',value=str(message.guild.owner))
        em.add_field(name='Membercount',value=str(message.guild.member_count))
        em.add_field(name='Large',value=str(message.guild.large))
        em.add_field(name='Created at',value=str(message.guild.created_at.strftime('%a, %-d %b %Y at %H:%M:%S GMT')))
        em.set_footer(text='ID: ' + str(message.guild.id),icon_url=message.guild.icon_url)
        await message.channel.send(embed=em)


client.run(token)
