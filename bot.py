import discord
import time
import random
import os
import cv2 as cv
# from discord import message
import asyncio
import csv
import sqlite3

import numpy as np
import pytesseract
import re
from private.config import TOKEN
from textPrep import grayMask, redMask, whiteMask
from databasething import *

from discord.ext import commands
from discord.ext.commands import has_permissions
from autocorrect import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
client = commands.Bot(command_prefix = '.',case_insensitive=True)
image_types = ["png", "jpeg", "gif", "jpg"]
methods = ['RedWhiteMaskBinary','RedWhiteMaskNoBinary','RedMaskNoBinary','RedMaskBinary','GrayMaskNoBinary','GrayMaskBinary','RegularThreshold','failure']
rings = ['Archers Ring','Berserker Ring','Warrior Ring','Seers Ring']


@client.event
async def on_ready():
    print('Bot is ready')
# Temporary commands

@client.command()
@has_permissions(administrator=True)
async def setup(ctx, *args):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("""CREATE TABLE ringtable (
                ringname text,
                tally integer
                )""")

    c.execute("INSERT INTO ringtable VALUES ('Berserker Ring',0)")
    c.execute("INSERT INTO ringtable VALUES ('Archers Ring',0)")
    c.execute("INSERT INTO ringtable VALUES ('Seers Ring',0)")
    c.execute("INSERT INTO ringtable VALUES ('Warrior Ring',0)")
    c.execute("SELECT * FROM ringtable ORDER BY tally DESC")
    ringlist = c.fetchall()
    print(ringlist)
    conn.commit()
    conn.close()

    return



@client.command()
async def tally(ctx):
    
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()

    #database code goes in here
    
    c.execute("SELECT * FROM ringtable ORDER BY tally DESC")
    ringlist = c.fetchall()
    ringname,ringnumber = zip(*ringlist)
    ringstring = ''

    for i in range(len(ringname)):
        ringstring = ringstring + '**'+str(ringname[i]) + 's found**: ' + str(ringnumber[i]) + '\n'
    await ctx.send(ringstring)
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def addbring(ctx,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    name = 'Berserker Ring'
    #database code goes in here
    player,pointsNew = addring(name,number)
    await ctx.send(f"{number} {player[0]} Has been added to the tally. The total is now {pointsNew}")
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def addaring(ctx,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    name = 'Archers Ring'
    #database code goes in here
    player,pointsNew = addring(name,number)
    await ctx.send(f"{number} {player[0]} Has been added to the tally. The total is now {pointsNew}")
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def addwring(ctx,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    name = 'Warrior Ring'
    #database code goes in here
    player,pointsNew = addring(name,number)
    await ctx.send(f"{number} {player[0]} Has been added to the tally. The total is now {pointsNew}")
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def addsring(ctx,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    name = 'Seers Ring'
    #database code goes in here
    player,pointsNew = addring(name,number)
    await ctx.send(f"{number} {player[0]} Has been added to the tally. The total is now {pointsNew}")

    

    return

def addring(name,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    #database code goes in here
    c.execute("SELECT * FROM ringtable WHERE ringname = :name" ,{'name': name})
    player = c.fetchone()
    pointsNew = int(number) + int(player[1])
    c.execute("""UPDATE ringtable SET tally = :points
                WHERE ringname = :name""",
                {'name':player[0],'points':pointsNew})
    
    conn.commit()
    conn.close()
    return player,pointsNew


@client.command()
@has_permissions(manage_roles=True)
async def removesring(ctx,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    name = 'Seers Ring'
    #database code goes in here
    player,pointsNew = removethering(name,number)
    await ctx.send(f"{number} {player[0]} Has been removed from the tally. The total is now {pointsNew}")
    return



@client.command()
@has_permissions(manage_roles=True)
async def removearing(ctx,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    name = 'Archers Ring'
    #database code goes in here
    player,pointsNew = removethering(name,number)
    await ctx.send(f"{number} {player[0]} Has been removed from the tally. The total is now {pointsNew}")
    return



@client.command()
@has_permissions(manage_roles=True)
async def removebring(ctx,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    name = 'Berserker Ring'
    #database code goes in here
    player,pointsNew = removethering(name,number)
    await ctx.send(f"{number} {player[0]} Has been removed from the tally. The total is now {pointsNew}")
    return


@client.command()
@has_permissions(manage_roles=True)
async def removewring(ctx,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    name = 'Warrior Ring'
    #database code goes in here
    player,pointsNew = removethering(name,number)
    await ctx.send(f"{number} {player[0]} Has been removed from the tally. The total is now {pointsNew}")
    return






def removethering(name,number = 1):
    conn = sqlite3.connect('rings.db')
    c=conn.cursor()
    #database code goes in here
    c.execute("SELECT * FROM ringtable WHERE ringname = :name" ,{'name': name})
    player = c.fetchone()
    pointsNew = int(player[1]) - int(number)
    c.execute("""UPDATE ringtable SET tally = :points
                WHERE ringname = :name""",
                {'name':player[0],'points':pointsNew})
    
    conn.commit()
    conn.close()
    return player,pointsNew
    












# Commands

@client.command()
async def pointHelp(ctx):
    await ctx.send("""Here is a list of implemented point commands:
                    \n.addPlayer name
                    \n.removePlayer name
                    \n.add name points
                    \n.remove name points
                    \n.points name
                    \n.setPoints name points
                    \n.setNickname name nickname
                    \n.setName name newname
                    \n.top10
                    \n.top50 """)


@client.command()
@has_permissions(manage_roles=True)
async def newDBTABLE(ctx, *args):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("""CREATE TABLE players (
                name text,
                nickname text,
                points integer
                )""")

    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(administrator=True)
async def alter(ctx):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    # c.execute("ALTER TABLE players ADD COLUMN nickname2 text DEFAULT ''")
    # c.execute("ALTER TABLE players ADD COLUMN nickname3 text DEFAULT ''")
    # c.execute("ALTER TABLE players ADD COLUMN nickname4 text DEFAULT ''")
    # c.execute("ALTER TABLE players ADD COLUMN nickname5 text DEFAULT ''")
    # c.execute("SELECT * FROM players ORDER BY points DESC")
    await ctx.send("This function is not active")


    conn.commit()
    conn.close()

    return



@client.command()
@has_permissions(manage_roles=True)
async def addPlayer(ctx, name):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    # check to see if a player exists
    c.execute("SELECT * FROM players WHERE name = :name",{'name': name})
    player = c.fetchone()
    if(player != None):
        await ctx.send(f"Player {name} already exists")
    else:
        c.execute("INSERT INTO players VALUES (:name, :nickname1, :points,:nickname2,:nickname3,:nickname4,:nickname5)",{'name': name,'nickname1':name,'points':0,'nickname2':'','nickname3':'','nickname4':'','nickname5':''})
        await ctx.send(f"Player {name} has been added.")

    # if its a new player, add them with default values
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def removePlayer(ctx, name):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here

    c.execute("DELETE from players WHERE name = :name",{'name': name})
    await ctx.send(f"Player {name} has been deleted")
    conn.commit()
    conn.close()

    return

@client.command()
@has_permissions(manage_roles=True)
async def add(ctx, name,points):
    player = namecheck(name)
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here

    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name points")
    else:
        pointsNew = int(points) + int(player[2])
        c.execute("""UPDATE players SET points = :points
                    WHERE name = :name""",
                    {'name':player[0],'points':pointsNew})
        await ctx.send(f"{points} points have been added to {player[0]}. Their new points total is {pointsNew}")

    conn.commit()
    conn.close()

    return

@client.command()
@has_permissions(manage_roles=True)
async def addpoints(ctx, name,points):
    player = namecheck(name)
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name points")
    else:
        pointsNew = int(points) + int(player[2])
        c.execute("""UPDATE players SET points = :points
                    WHERE name = :name""",
                    {'name':player[0],'points':pointsNew})
        await ctx.send(f"{points} points have been added to {player[0]}. Their new points total is {pointsNew}")

    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def remove(ctx, name, points):
    player = namecheck(name)
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here

    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name points")
    else:
        
        pointsNew = int(player[2]) - int(points)
        if pointsNew < 0: pointsNew = 0
        c.execute("""UPDATE players SET points = :points
                    WHERE name = :name""",
                    {'name':player[0],'points':pointsNew})
        await ctx.send(f"{points} points have been removed from {player[0]}. Their new points total is {pointsNew}")
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def removepoints(ctx, name, points):
    player = namecheck(name)
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name points")
    else:
        
        pointsNew = int(player[2]) - int(points)
        if pointsNew < 0: pointsNew = 0
        c.execute("""UPDATE players SET points = :points
                    WHERE name = :name""",
                    {'name':player[0],'points':pointsNew})
        await ctx.send(f"{points} points have been removed from {player[0]}. Their new points total is {pointsNew}")
    conn.commit()
    conn.close()

    return


@client.command()
async def points(ctx, name):
    player = namecheck(name)
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here

    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name")
    else:
        await ctx.send(f'The player {player[0]} has {player[2]} points.')

    
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def setPoints(ctx, name, points0):
    points = int(points0)
    if(points <0):
        await ctx.send('Cannot have negative points')
        return
    
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("SELECT * FROM players WHERE name = :name OR nickname = :nickname",{'name': name, 'nickname':name})
    player = c.fetchone()
    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name points")
        
    else:
        c.execute("""UPDATE players SET points = :points
                    WHERE name = name = :name OR nickname = :nickname""",
                    {'name':name,'nickname':name,'points':points})
        await ctx.send(f"The points of {name} have been set to {points}")

    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def setNickname(ctx, name,nickname):
    
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("SELECT * FROM players WHERE name = :name",{'name': name})
    player = c.fetchone()
    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name nickname")
    else:
        c.execute("UPDATE players SET nickname = :nickname WHERE name = :name",{'name': name,'nickname': nickname})
        await ctx.send(f"The nickname of {name} have been set to {nickname}")
    conn.commit()
    conn.close()

    return

@client.command()
@has_permissions(manage_roles=True)
async def addNickname(ctx, name,nickname):
    
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("SELECT * FROM players WHERE name = :name",{'name': name})
    player = c.fetchone()
    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name nickname")
    else:
        print('we before the for loop')
        for idx, nicknameslot in enumerate(player[3:7]):
            print('in the for loop, nicknameslot,idx: '+nicknameslot+','+str(idx))
            if nicknameslot == '':
                slot = idx + 2
                c.execute("UPDATE players SET nickname"+ str(slot)+" = :nickname WHERE name = :name",{'name': name,'nickname': nickname})
                await ctx.send(f"The nickname of {name} have been set to {nickname} in nickname slot {slot}")
                conn.commit()
                conn.close()
                return
        # c.execute("UPDATE players SET nickname = :nickname WHERE name = :name",{'name': name,'nickname': nickname})
        # await ctx.send(f"The nickname of {name} have been set to {nickname}")
    conn.commit()
    conn.close()

    return


# @client.command()
# @has_permissions(manage_roles=True)
# async def clearDatabaseYesReally74918274(ctx):
#     conn = sqlite3.connect('powerpoints.db')
#     c=conn.cursor()

#     #database code goes in here
#     # c.execute("DELETE FROM players")
#     conn.commit()
#     conn.close()

#     return



@client.command()
async def top10(ctx):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("SELECT * FROM players ORDER BY points DESC")
    players = c.fetchmany(10)
    name,nickname,points,x2,x3,x4,x5 = zip(*players)
    leaderboard = ''

    for i in range(len(name)):
        leaderboard = leaderboard + str(name[i]) + ' -- ' + str(points[i]) + '\n'
    await ctx.send(f"**Top 10 leaderboard:**\n{leaderboard}")
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def top50(ctx):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("SELECT * FROM players ORDER BY points DESC")
    players = c.fetchmany(50)
    name,nickname,points,x2,x3,x4,x5 = zip(*players)
    leaderboard = ''

    for i in range(len(name)):
        leaderboard = leaderboard + str(name[i]) + ' -- ' + str(points[i]) + '\n'
    await ctx.send(f"**Top 50 leaderboard:**\n{leaderboard}")
    conn.commit()
    conn.close()

    return



@client.command()
@has_permissions(manage_roles=True)
async def fetchall(ctx):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("SELECT * FROM players ORDER BY name ASC")
    players = c.fetchall()
    name,nickname,points = zip(*players)
    leaderboard = ''
    print(name)
    for i in range(len(name)):
        leaderboard = leaderboard + str(name[i]) + '\n'
    await ctx.send(f"**All players:**\n{leaderboard}")
    conn.commit()
    conn.close()

    return



@client.command()
@has_permissions(manage_roles=True)
async def summary(ctx,name):
    player = namecheck(name)
    
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    
    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name")
    else:
        await ctx.send(player)

    conn.commit()
    conn.close()

    return



@client.command()
@has_permissions(manage_roles=True)
async def newplayers(ctx):
    with open('oldplayers.csv',newline='') as csvfile:
        oldplayers = list(csv.reader(csvfile))


    with open('currentplayers.csv',newline='') as csvfile:
        currentplayers = list(csv.reader(csvfile))

    newplayers = [i for i in currentplayers + oldplayers if i not in currentplayers]
    newplayers.sort()
    await ctx.send("Players to remove \n" + str(newplayers))

    newplayers = [i for i in currentplayers + oldplayers if i not in oldplayers]
    newplayers.sort()
    await ctx.send("Players to add \n" + str(newplayers))
    return










@client.command()
@has_permissions(manage_roles=True)
async def setName(ctx, name,newname):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here
    c.execute("SELECT * FROM players WHERE name = :name",{'name': name})
    player = c.fetchone()
    if(player == None):
        await ctx.send(f"Couldn't find player {name}. Ensure you type .command name nickname")
    else:
        c.execute("UPDATE players SET name = :name WHERE nickname = :nickname AND points = :points",{'name': newname,'nickname': player[1],'points':player[2]})
        await ctx.send(f"The name of {name} have been set to {newname}")
    
    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def link(ctx, user:discord.User):
    await ctx.send(user.id)
    
    return



@client.command()
@has_permissions(manage_roles=True)
async def eventpoints(ctx, *args):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here

    conn.commit()
    conn.close()

    return



@client.command()
@has_permissions(manage_roles=True)
async def pointBan(ctx, *args):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here

    conn.commit()
    conn.close()

    return



@client.command()
@has_permissions(manage_roles=True)
async def undo(ctx, *args):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here

    conn.commit()
    conn.close()

    return


@client.command()
@has_permissions(manage_roles=True)
async def generateSheet(ctx, *args):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()

    #database code goes in here

    conn.commit()
    conn.close()

    return




# end point commands
# fun commands

@client.command()
async def motivation(ctx):
    rare_drop = random.randint(0,5000)
    if(rare_drop == 1):
        await ctx.send('Dumb rat, give up, ya shit cunt.')
        return
    random_phrase_1 = random.choice(motivation1)
    random_phrase_2 = random.choice(motivation2)
    random_phrase_3 = random.choice(motivation3)
    random_phrase_4 = random.choice(motivation4)
    await ctx.send(f'{random_phrase_1} {random_phrase_2} {random_phrase_3} {random_phrase_4}')

# end fun commands

@client.command()
async def correct(ctx, *args):
    await ctx.send(f'You sent:  {args}')
    listargs = list(args)
    correction = []
    for word in listargs:
        print(word)
        correction = autoCorrect(word,database)
        print(correction)
    await ctx.send(f'Correction is: {correction}')
    #await ctx.send(f'Pong!{round(client.latency*1000)}')

@client.command()
async def extract(ctx, *args):
    str = ' '.join(args)
    text = extractInformation2(str)
    await ctx.send(f'**Extracted information is:**\n{text}')


@client.command()
async def react(ctx):
    
    msg = await ctx.send('Choose a reaction')
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

    def checkThumbup(reaction,user):
        return str(reaction.emoji) =='👍' and user == ctx.author
    
    try:
        reaction,user = await client.wait_for('reaction_add',timeout = 10.0,check = checkThumbup)
    except asyncio.TimeoutError:
        await ctx.send('You took too long')
    else:
        await ctx.send('You reacted with a thumb up')

@client.command()
async def read(ctx):
    content = ctx.message.attachments
    if len(content):
        for attachment in ctx.message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save('temp.png')
    else:
        #insert randomness for random insult
        # await ctx.send('no img')
        await ctx.send(random.choice(list(insults)))
        return
    process = 1
    processChoice = imagePrepareSwitcher()

    text = []
    img = cv.imread('temp.png',-1)

    # img = cv.bitwise_not(img1)

    while (process <8):
        readImage = processChoice.indirect(img,process)
        newtext = pytesseract.image_to_string(readImage)
        text.append(newtext)
        process += 1
    outputtext = max(text,key=len)
    
    await ctx.send(f'**The read text is: **\n\n{outputtext}')

@client.command()
async def codeword(ctx):
    #this function chooses a random code word for bingo and other events
    #it currently sucks, can probably be done in a single line but its 
    #super rare that it gets called so i cba optimizing
    with open("google-10000-english.txt", "r") as file:
        allText = file.read()
        words = list(map(str, allText.split()))
        inadequateWord = True
        while inadequateWord:
            wordchoice = random.choice(words)
            if len(wordchoice) < 4: continue
            else: inadequateWord = False
    await ctx.send(f'Your codeword is: {wordchoice}')

@client.command()
async def clear(ctx, amount = 2):
    if ctx.guild.id == 532377514975428628: #stops it working in rng street
        return
    if type(amount) == 'str':
        if amount.lower() == 'all':
            amount1 = 9
        else: 
            await ctx.send('Please enter a valid integer')
            return
    else: amount1 = amount
    await ctx.send('coming soon')
    # await ctx.channel.purge(limit = amount)
    
@client.command()
async def forceRead(ctx, num):
    content = ctx.message.attachments
    if len(content):
        for attachment in ctx.message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save('temp.png')
    else:
        #insert randomness for random insult
        # await ctx.send('no img')
        await ctx.send(random.choice(list(insults)))
        return
    
    processChoice = imagePrepareSwitcher()
    img = cv.imread('temp.png',-1)
    choice = int(num)
    readImage = processChoice.indirect(img,choice)
    text=pytesseract.image_to_string(readImage)

    keyInfo = extractInformation2(text)


    if keyInfo == '':
        keyInfo = '*Could not read any valuable information*'
        # await channel.send('Red white mask\n'+text + '\n\n'+"**"+'Useful information:'+"**"+'\n'+correctedText)
    await ctx.send('**'+methods[choice]+'**\n' + '\n\n**Extracted information**\n'+keyInfo +'\n\n**Is this correct?**')

#end of commands

@client.event
async def on_reaction_add(reaction,user):
    
    return

@client.event
async def on_message(message):
    if message.author.bot: #ensures no recursion
        return
    
    channel = message.channel
    if (channel.name != 'phat-loot-and-achievements') and (channel.name != 'clan-scrapbook')and (channel.name != 'combat-diaries') and (channel.name != 'group-ironman'): #limits channels
        await client.process_commands(message) #ensures commands still work
        return
    content = message.attachments #attachments is a list datatype
    # await channel.send('Say hello!')
    if len(content):
        
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save('temp.png')

        img = cv.imread('temp.png',-1)
        # img = cv.Canny(img1,150,200)
        keyInfo = ''
        keyInfo2 = []
        keyInfoRings = []
        process = 1
        processChoice = imagePrepareSwitcher()
        while (process <8): #(keyInfo == '') and 

            readImage = processChoice.indirect(img,process)
            text = pytesseract.image_to_string(readImage)

            # keyInfo = extractInformation2(text)
            keyInfo2.append(extractInformation2(text))
            # keyInfoRings.append(extractInformation2(text,False,rings))
            process += 1
        ######writes image and sends it
        # cv.imwrite("binaryimg.png",readImage)
        # await channel.send(file=discord.File('binaryimg.png'))
        # if keyInfo2 == []:
        # #    keyInfo = '*Could not read any valuable information*'
        #     outputtext = '*Could not read any valuable information*'

        #     process +=1
        # else: 
        #     outputtext = max(keyInfo2,key=len)
        #     process = keyInfo2.index(max(keyInfo2,key=len))
        
        outputtext = max(keyInfo2,key=len)
        print(outputtext)
        if outputtext == '':
            outputtext = '*Could not read any valuable information*'
            process =len(methods)-1 #the last value of methods will always be failure
        else: 
            process = keyInfo2.index(max(keyInfo2,key=len))
        # readimage = processChoice.indirect(img,process+1)
        # cv.imwrite("binaryimg.png",readimage)
        # await channel.send(file=discord.File('binaryimg.png'))
        
        
        #######DKS EVENT##########
        # print(keyInfoRings)
        # outputringtext = max(keyInfoRings,key=len)
        # if outputringtext == '':
        #     print('no ring detected')
        # else:
        #     channel=client.get_channel(893362449565241354) #dks pet race channel in main server::::::::bot server: 893036776803942422    main server:893362449565241354
        #     await channel.send(message.jump_url)
        #     print(outputringtext)
        #     ringname = autoCorrect(outputringtext,rings)
        #     print(ringname)
        #     ringname,newtotal = addring(ringname)
        #     await channel.send(f'One {ringname[0]} has been added! New total is {newtotal}')
        
        # channel = client.get_channel(868036300622676028) #bot channel on testing server
        id = message.guild.id
        if id == 532377514975428628: #this is rng street guild id
            channel = client.get_channel(714026607550922773) #bot channel on bot server street  893036776803942422    714026607550922773   
        
        await channel.send(file=discord.File('temp.png'))
        
        # await channel.send('**'+methods[process-2]+'**\n' + '\n\n**Extracted information**\n'+keyInfo +'\n\n**Is this correct?**')
        msg = await channel.send(f'**{methods[process]}**\n \n\n**Extracted information**\n{outputtext} \n\n**React with 👎 if this is incorrect**')
        
        await msg.add_reaction("👎")
        def checkThumbDown(reaction,user):
            return str(reaction.emoji) =='👎' and not(user.bot)
    
        try:
            reaction,user = await client.wait_for('reaction_add',timeout = 120.0,check = checkThumbDown)
        except asyncio.TimeoutError:
            return
        else:
            await channel.send(f'Thank you, {user}. Sending error report')
            if os.path.exists('failures/errorReport.png'):
                # plt.savefig('/failures/errorReport_{}.png'.format(int(time.time())))
                cv.imwrite('failures/errorReport_{}.png'.format(int(time.time())),img)
            else:
                cv.imwrite('failures/errorReport.png',img)
            # await message.add_reaction()



        


        
    
    await client.process_commands(message) #ensures commands still work


def namecheck(name):
    conn = sqlite3.connect('powerpoints.db')
    c=conn.cursor()
    c.execute("SELECT * FROM players ORDER BY name ASC")
    players = c.fetchall()
    namelist,nickname1,points,nickname2,nickname3,nickname4,nickname5 = zip(*players)
    namebase = namelist + nickname1+nickname2+nickname3+nickname4+nickname5
    newname = autoCorrect(name,namebase,0.75)
    print(newname)

    c.execute("""SELECT * FROM players WHERE name = :name 
                OR nickname1 = :name
                OR nickname2 = :name 
                OR nickname3 = :name 
                OR nickname4 = :name 
                OR nickname5 = :name""",{'name': newname})
    player = c.fetchone()
    conn.commit()
    conn.close()
    
    return player


class imagePrepareSwitcher(object):
    # all the cases of image processing for use in a loop
    def indirect(self,img,i):
        method_name = 'number_'+str(i)
        method=getattr(self,method_name,lambda x:img)
        return method(img)
    def number_1(self,img):
        return maskRedWhite(img,1)
    def number_2(self,img):
        return maskRedWhite(img,0)
    def number_3(self,img):
        return maskRed(img,0)
    def number_4(self,img):
        return maskRed(img,1)
    def number_5(self,img):
        return maskGray(img,0)
    def number_6(self,img):
        return maskGray(img,1)
    def number_7(self,img):
        return regThreshold(img)
    
def maskRedWhite(img,binary = 0,upper = 255,lower = 65):
    mask = redMask(img)+whiteMask(img)
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    if(binary):
        output_imgbw = cv.cvtColor(output_img, cv.COLOR_BGR2GRAY)
        ret,output = cv.threshold(output_imgbw,lower,upper,cv.THRESH_BINARY)
        return output
        
    return output_img

def maskRed(img,binary = 0,upper = 255,lower = 65):
    mask = redMask(img)
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    
    if(binary):
        output_imgbw = cv.cvtColor(output_img, cv.COLOR_BGR2GRAY)
        ret,output = cv.threshold(output_imgbw,lower,upper,cv.THRESH_BINARY)
        return output
        
    return output_img

def maskGray(img,binary = 0,upper = 255,lower = 65):
    mask = grayMask(img)
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
    
    if(binary):
        output_imgbw = cv.cvtColor(output_img, cv.COLOR_BGR2GRAY)
        ret,output = cv.threshold(output_imgbw,lower,upper,cv.THRESH_BINARY)
        return output
        
    return output_img

def regThreshold(img,upper = 255,lower = 125):
    output_imgbw = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret,output2 = cv.threshold(output_imgbw,lower,upper,cv.THRESH_BINARY)
    return output2


def extractKeyphrase(text,database = database):
    text2 = text.splitlines()
    correctedText = ''
    previouscorrect = ''
    for line in text2:
        autocorrectline = autoCorrect(line,database,0.7)
        if (autocorrectline != line) and (previouscorrect != autocorrectline) :
            correctedText = correctedText + autocorrectline
            previouscorrect = autocorrectline
        else:
            continue

    return correctedText

def extractInformation(text,extractionVal = '[0-9]+'):
    text2 = text.splitlines()
    value = re.compile(extractionVal)
    correctedText = ''
    extractionOut = ''
    lastline = ''
    count = 1
    for line in text2:
        m = len(line)
        for n in range(m):
            bigGram = ngram(line,n,' ')
            extraction = extractKeyphrase(bigGram)
            if (extraction != '')and(line != lastline):
                lastline = line
                # print(f'line{count} = {line}')
                # print(line.partition(bigGram))
                # extractionOut = extractionOut+extraction
                # next thing to do is check to see if modulo the value by 100 is 
                # 0, then if the number divided by 100, then modulo 5 (500, 1000, 1500)
                # return extraction + ''.join(value.findall(line))
                extractionOut = extractionOut + extraction +' '+ ''.join(value.findall(line)) + '\n'
        lastline = line
        count +=1
            

    return extractionOut


def extractInformation2(text,includeNumbers = True,wordbase = database,extractionVal = '[0-9]+'):
    text2 = text.splitlines()
    value = re.compile(extractionVal)
    correctedText = ''
    extractionOut = ''
    lastline = ''
    count=1
    for line in text2:
        m = len(line)
        for n in range(m):
            bigGram = ngram(line,n,' ')
            extraction = extractKeyphrase(bigGram,wordbase)
            if (extraction != '')and(line != lastline):
                lastline = line
                if includeNumbers:
                    if(extraction.find('loot')>=0) or (extraction.find('kill')>=0) or (extraction.find('lap')>=0) or (extraction.find('teasure')>=0) or (extraction.find('received')>=0):
                        #this is a general case for loot, kc, laps etc excluding valuable drop and level
                        colonsplit = re.compile(':')
                        splitline = colonsplit.split(line)
                        lineparse = splitline[-1] #the last postion; the numbers will be at the end

                    elif(extraction.find('Valuable')>=0):
                        #specifically for valuable drop
                        colonsplit = re.compile(':')
                        splitline = colonsplit.split(line) #split the string at the colon
                        secondhalf = splitline[-1]

                        bracketsplit = re.compile(r'\(')
                        coinvalue = bracketsplit.split(secondhalf) #split the string at the bracket
                        lineparse = coinvalue[-1]
                    elif(extraction.find('feel')>=0):
                        lineparse = extraction
                    else:
                        #specifically for levels
                        lineparse = line
                    # x = line.split()
                    # x = colon.findall(line)
                    outPutNumber = ''.join(value.findall(lineparse))
                    if outPutNumber =='':
                        keyValue = 0
                    else:
                        keyValue = int(outPutNumber)
                    powerPoints = int(pointCalcNew(extraction,keyValue)) #some values might come back float so force int
                    # extractionOut = extractionOut+extraction
                    # next thing to do is check to see if modulo the value by 100 is 
                    # 0, then if the number divided by 100, then modulo 5 (500, 1000, 1500)
                    # return extraction + ''.join(value.findall(line))
                    extractionOut = extractionOut + extraction +' '+ outPutNumber + ' for '+str(powerPoints)+' power points.\n'
                else:
                    extractionOut = extractionOut + extraction +'\n'
        lastline = line
        count+=1
            

    return extractionOut

def ngram(text,n=2,spacer = ''):
    newtext = text.replace('\n',' ')
    biwordgrams = create_ngram(newtext.split(),n,spacer)
    return "\n".join(biwordgrams)

def localBigram(text):
    newtext = text.replace('\n',' ')
    biwordgrams = create_bigram2(newtext.split(),' ')
    return "\n ".join(biwordgrams)

def pointCalc(text,number):
    gazornogaz = 0
    if(text.find('drop') >=0) or (text.find('loot') >=0)or (text.find('treasure') >=0): # if it's a valuable drop
        
        if(number < 50000000):
            if(number<10000000):
                if(number <1000000):
                    if(number <100000):
                        return 0
                    return 1
                return 3
            return 5
        return 10
    elif(text.find('kill') >= 0 ) or (text.find('lap') >= 0 ): #for lap counters and killcounts
        
        if number == 0: return 0 #error case

        if(number == 100):
            return 3
        elif(number == 2500):
            return 10
        elif (number%500 ==0):
            return 5
        else:
            return 0
    elif(text.find('followed') >= 0 ) or (text.find('sneaking') >= 0 ): #for pets
        if text.find('would') >=0:
            return 10
        else:
            return 20
    elif(text.find('level') >=0): # for levels
        if number == 0: return 0 #error case

        if number == 99: return 10

        if (number%5 == 0) and (number >=  70): return 5

        if (text.find('runecrafting') >=0) and number == 77: return 3
        if (text.find('construction') >=0) and number == 83: return 3
        if (text.find('prayer') >=0) and number == 77: return 3
    elif(text.find('Chambers') >= 0 ) or (text.find('Coffin') >= 0 ):
        if number == 0: return 0 #error case
        if(number == 10): return 3
        if(number%250 ==0):return 10
        if(number%50 == 0):return 5
        else: return 0
    return gazornogaz

def pointCalcNew(text1,number):
    gazornogaz = 0
    text = text1.lower()
    if(text.find('drop') >=0) or (text.find('loot') >=0) or (text.find('treasure') >=0): # if it's a valuable drop
        
        if(number < 100000000): #100m
            if(number<50000000): #50m
                if(number <25000000): #25m
                    if(number <10000000): #10m
                        if(number <5000000): #5m
                            if(number <1000000): #1m
                                if(number <100000): #100k
                                    return 0
                                return 1
                            return 2
                        return 3
                    return 4
                return 6
            return 8
        return 10
    elif (text.find('kill') >= 0 ): #forkillcounts
        
        if number == 0: return 0 #error case

        if(number == 100):
            return 3
        elif(number%1000 == 0):
            return 10
        elif (number%500 ==0):
            return 5
        else:
            return 0
    elif (text.find('lap') >= 0 ):
        if number == 0: return 0 #error case

        if(number%500 == 0): return 1
        else: return 0
    elif (text.find('chambers') >= 0 ) or (text.find('theatre') >= 0 ) or (text.find('hallowed') >= 0 ) or (text.find('gauntlet') >= 0 ):
        if number == 0: return 0 #error
        
        if number == 10: return 3 #first 10
        elif (number%250 == 0): return 10 #every 250
        elif (number%50 == 0): return 5 #every 50
    elif (text.find('followed') >= 0 ) or (text.find('sneaking') >= 0 ): #for pets
        if text.find('would') >=0:
            return 10
        else:
            return 20
    elif (text.find('level') >=0): # for levels
        if (number == 0) or (number > 99): return 0 #error case

        if (text.find('agility') >= 0 ) or (text.find('runecrafting') >= 0 ) or (text.find('mining') >= 0 ) or (text.find('slayer') >= 0 ):
            if (number == 99): return 20
            if (number >= 50) and (number%5 ==0):
                return (number -50)/5 + 1 # should be 50 = 1 55 = 2 60 = 3 etc up to 95
        elif (text.find('prayer') >= 0 ) or (text.find('hunter') >= 0 ) or (text.find('construction') >= 0 ) or (text.find('crafting') >= 0 ) or (text.find('herblore') >= 0 ) or (text.find('fishing') >= 0 ) or (text.find('woodcutting') >= 0 ):
            if (number == 99): return 15
            if (number >= 50) and (number%5 ==0):
                return (number -60)/5 + 1 # should be 60 = 1 65 = 2 70 = 3 etc up to 95
        elif (text.find('attack') >= 0 ) or (text.find('strength') >= 0 ) or (text.find('defence') >= 0 ) or (text.find('hitpoints') >= 0 ) or (text.find('ranged') >= 0 ) or (text.find('magic') >= 0 ) or (text.find('thieving') >= 0 ) or (text.find('smithing') >= 0 ) or (text.find('farming') >= 0 ):
            if (number == 99): return 10
            if (number >= 50) and (number%5 ==0):
                return (number -65)/5 + 1 # should be 65 = 1 70 = 2 75 = 3 etc up to 95
        elif (text.find('fletching') >= 0 ) or (text.find('cooking') >= 0 ) or (text.find('firemaking') >= 0 ):
            if (number == 99): return 10
            if (number >= 80) and (number%5 ==0):
                return (number -60)/5 + 1 # should be 80 = 1 85 = 2 90 = 3 etc up to 95
        else: return 0
    elif (text.find('combat task')>=0) or (text.find('combat achievement') >=0):
        if (text.find('completed all')>=0): # full tier completion
            if (text.find('easy')>=0): return 3
            elif (text.find('medium')>=0): return 5
            elif (text.find('hard')>=0): return 7
            elif (text.find('elite')>=0): return 10
            elif (text.find('master')>=0): return 15
            elif (text.find('grandmaster')>=0): return 20
        elif (text.find('master')>=0): 
            if (text.find('grandmaster')>=0): return 2 #completed a grandmastermaster combat task
            return 1 #completed a master combat task
    return gazornogaz


client.run(TOKEN)
