# bot.py
import os
from discord import channel
from discord.ext import tasks
import requests
import time
import sched

import discord
TOKEN = ''
GUILD = ''
rsnList = {'477469957710544897':'artliquid', '171172513345306624':'SneakyPete', '278770482965250048':'pet rol'}
xpPerPoint = 1000
currentTotalXP = {}
previousTotalXP = {}
currentBossKC = {}
previousBossKC = {}
powerPoints = {}



client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    await init()
    update.start()
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'

    
    )

async def init():
    for key,value in rsnList.items():
        totalXP = await getTotalXP(value)
        bossKC = await getBossKC(value)
        currentTotalXP.update({key : totalXP})
        previousTotalXP.update({key : totalXP})
        currentBossKC.update({key : bossKC})
        previousBossKC.update({key : bossKC})
        powerPoints.update({key : 0})
    print('Initialization complete.')
    postChannel = client.get_channel(886128033029836810)
    #await postChannel.send('I am here')

async def getTotalXP(username):
    response = requests.get('https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + username).text
    totalXP = response.split('\n')[0].split(',')[2]
    return int(totalXP)

async def getBossKC(username):
    response = requests.get('https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + username).text.split('\n')
    del response[:36]
    del response[-1]
    bossKC = 0
    for boss in response:    
        kc = boss.split(',')[1]
        bossKC += int(kc)
    return bossKC


async def updatePowerPoints(user, pointGain):
    try:
        currentPoints = powerPoints.get(user)
    except:
        currentPoints = 0
    powerPoints.update({user :currentPoints + pointGain})

@tasks.loop(minutes=1)
async def update():           
    for key,value in rsnList.items():
        totalXP = await getTotalXP(value)
        xpDiff = totalXP - previousTotalXP.get(key)
        xpPointGain = round(xpDiff * 0.1, 1)

        bossKC = await getBossKC(value)
        kcPointGain = bossKC - previousBossKC.get(key)

        print(value)
        print(totalXP)
        print(xpDiff)
        print(xpPointGain)
        print(kcPointGain)


        if(xpPointGain >= 0.1):
            currentTotalXP.update({key : int(totalXP)})
            powerPoints.update({key : xpPointGain + powerPoints.get(key)})

        if(kcPointGain >= 1):
            currentBossKC.update({key : int(bossKC)})
            powerPoints.update({key : kcPointGain + powerPoints.get(key)})

    await updateChannelPost()

async def updateChannelPost():
    print("Updating")
    post = ''
    titleM1 = '```Recent Updates:```\n'
    userM1 = ' has gained '
    userM2 = ' Total XP and '
    userM4 = ' Boss KC. '
    userM3 = ' power points have been awarded.\n'
    blockM1 = '\n```Leaderboard:```\n'

    post = titleM1
    
    #Changed XP
    for id,rsn in rsnList.items():
        xpDiff = currentTotalXP.get(id) - previousTotalXP.get(id)
        kcDiff = currentBossKC.get(id) - previousBossKC.get(id)
        id = '<@' + id + '>'
        pointGain = round(xpDiff * 0.1, 1) + kcDiff
        if(pointGain >= 0.1):
            post += id + ': **' + rsn + '** ' + userM1 + str(xpDiff) + userM2 + str(kcDiff) + userM4 + str(pointGain) + userM3

    post += blockM1
    orderedList = sorted(powerPoints.items(), key=lambda x: x[1], reverse=True)
    i = 1
    for id,points in orderedList:
        rsn = rsnList.get(id)
        xp = "{:,}".format(currentTotalXP.get(id))
        kc = "{:,}".format(currentBossKC.get(id))
        idF = '<@' + id + '>'
        post += '**' + str(i) + '.  **' + idF + ' : **' + rsn + '**:\t\t' + str(points) + ' points\n'
        post += '\t\t\t\t\tTotalXP: ' + xp + '\t\t Boss KC: ' + kc + '\n'
        i+=1
    

    postChannel = client.get_channel(886128033029836810)
    msg = await postChannel.fetch_message(886128321149157376)
    await msg.edit(content=post)

    await resetGains()

async def resetGains():
    for key, value in currentBossKC.items():
        previousBossKC.update({key : value})
    for key, value in currentTotalXP.items():
        previousTotalXP.update({key : value})




client.run(TOKEN)