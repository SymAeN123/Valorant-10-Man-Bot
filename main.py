import os
import asyncio
import random
from itertools import chain

numArray = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

numDict = {"1️⃣": 0, "2️⃣": 1, "3️⃣": 2, "4️⃣": 3, "5️⃣": 4, "6️⃣": 5, "7️⃣": 6, "8️⃣": 7}

Maps = ["Bind", "Haven", "Split", "Ascent", "Icebox", "Breeze"]

Ranks = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Immortal", "Radiant", "Unranked"]

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix="v!")
Instances = 0

async def FindRole(member):
    Roles = member.roles
    for role in Roles:
        if role.name == "Iron":
            return 0
        elif role.name == "Bronze":
            return 1
        elif role.name == "Silver":
            return 2
        elif role.name == "Gold":
            return 3
        elif role.name == "Platinum":
            return 4
        elif role.name == "Diamond":
            return 5
        elif role.name == "Immortal":
            return 6
        elif role.name == "Radiant":
            return 7
    return 8

async def deletevc(ctx):
    guild = ctx.guild
    
    Name = "Match Created by: " + ctx.author.name
    Category = discord.utils.get(guild.categories, name=Name)
    
    if Category == None:
        await ctx.channel.send("That channel was not found.")
        return
    
    for i in range(1, -1, -1):
        await (Category.voice_channels)[i].delete()
        
    await Category.delete()
    
    return    

async def GetReaction(msg, arg, TIMEOUT, ctx):
    while 1: #get reaction
        if (TIMEOUT == 0):
            reaction = await client.wait_for("reaction_add")
        else:
            reaction = await client.wait_for("reaction_add", timeout=TIMEOUT)
        
        if type(arg) == type(1):        
            if (reaction[0].message != msg):
                continue
            elif (reaction[0].emoji == "❌") and (reaction[1].name == ctx.author.name):
                await ctx.channel.send("Exited.")
                return 1
            elif (reaction[0].count >= arg):
                break
        else:
            if (reaction[0].message != msg):
                continue
            elif (reaction[0].emoji == "❌") and (reaction[1].name == ctx.author.name):
                await ctx.channel.send("Exited.")
                return 1
            elif (reaction[1] == arg):
                break
    return reaction

async def MakeSelection(Attackers, Defenders, WaitingRoomMembers, a, b, msg, ctx):
    global Instances

    if len(WaitingRoomMembers) == 0:
        MessageStr = "---------------------\nFinal Picks:\n\n"
        MessageStr += "\nAttackers:\n"
        for member in Attackers:
            MessageStr += member.name + "#" + member.discriminator + " (" + Ranks[await FindRole(member)] + ")" + "\n"
        MessageStr += "\nDefenders:\n"
        for member in Defenders:
            MessageStr += member.name + "#" + member.discriminator + " (" + Ranks[await FindRole(member)] + ")" + "\n"
        await msg.edit(content=MessageStr)
        return

    if bool(a)^bool(b):
        MessageStr = "---------------------\n**Attacker's pick (captain only):**\n\n"
        MessageStr += "Availible picks:\n"
        for i in range(len(WaitingRoomMembers)):
            MessageStr += numArray[i] + ":   " + WaitingRoomMembers[i].name + "#" + WaitingRoomMembers[i].discriminator + " (" + Ranks[await FindRole(WaitingRoomMembers[i])] + ")" + "\n"
        MessageStr += "\nAttackers:\n"
        for member in Attackers:
            MessageStr += member.name + "#" + member.discriminator + " (" + Ranks[await FindRole(member)] + ")" + "\n"
        MessageStr += "\nDefenders:\n"
        for member in Defenders:
            MessageStr += member.name + "#" + member.discriminator + " (" + Ranks[await FindRole(member)] + ")" + "\n"
        await msg.edit(content=MessageStr)
        reaction = await GetReaction(msg, Attackers[0], 180, ctx)
        if reaction == 1:
            Instances -= 1
            print("Current Instances =", Instances)
            return 1
        Member = WaitingRoomMembers[numDict[reaction[0].emoji]]
        await msg.clear_reaction(emoji=numArray[len(WaitingRoomMembers) - 1], )
        Attackers.append(Member)
        WaitingRoomMembers.remove(Member)

    else:
        MessageStr = "---------------------\n**Defender's pick (captain only):**\n\n"
        MessageStr += "Availible picks:\n"
        for i in range(len(WaitingRoomMembers)):
            MessageStr += numArray[i] + ":   " + WaitingRoomMembers[i].name + "#" + WaitingRoomMembers[i].discriminator + " (" + Ranks[await FindRole(WaitingRoomMembers[i])] + ")" + "\n"
        MessageStr += "\nAttackers:\n"
        for member in Attackers:
            MessageStr += member.name + "#" + member.discriminator + " (" + Ranks[await FindRole(member)] + ")" + "\n"
        MessageStr += "\nDefenders:\n"
        for member in Defenders:
            MessageStr += member.name + "#" + member.discriminator + " (" + Ranks[await FindRole(member)] + ")" + "\n"
        await msg.edit(content=MessageStr)
        reaction = await GetReaction(msg, Defenders[0], 180, ctx)
        if reaction == 1:
            Instances -= 1
            print("Current Instances =", Instances)
            return 1
        Member = WaitingRoomMembers[numDict[reaction[0].emoji]]
        await msg.clear_reaction(emoji=numArray[len(WaitingRoomMembers) - 1], )
        Defenders.append(Member)
        WaitingRoomMembers.remove(Member)

async def MakeRandomSelections(Attackers, Defenders, WaitingRoomMembers, State):
    DividedWaitingRoom = [[],[],[],[],[],[],[],[],[]]
    for member in WaitingRoomMembers:
        Role = await FindRole(member)
        DividedWaitingRoom[Role].append(member)
    for i in range(len(DividedWaitingRoom)):
        if len(DividedWaitingRoom[i]) != 0:
            random.shuffle(DividedWaitingRoom[i])
    SortedWaitingRoom = list(chain.from_iterable(DividedWaitingRoom))
    State = random.choice([True, False])
    if State:
        Attackers.append(SortedWaitingRoom[0])
        SortedWaitingRoom.pop(0)
        State = not State
    else:
        Defenders.append(SortedWaitingRoom[0])
        SortedWaitingRoom.pop(0)
        State = not State
    while len(SortedWaitingRoom) != 0:
        if State:
            Attackers.append(SortedWaitingRoom[0])
            SortedWaitingRoom.pop(0)
            if len(SortedWaitingRoom) != 0:
                Attackers.append(SortedWaitingRoom[0])
                SortedWaitingRoom.pop(0)
            State = not State
        else:
            Defenders.append(SortedWaitingRoom[0])
            SortedWaitingRoom.pop(0)
            if len(SortedWaitingRoom) != 0:
                Defenders.append(SortedWaitingRoom[0])
                SortedWaitingRoom.pop(0)
            State = not State

async def ManageRoom(Attackers, Defenders, WaitingRoomMembers, msg, ctx, captain):
    global Instances
    guild = ctx.guild
    CategoryTitle = "Match Created by: " + ctx.author.name
    
    while 1: #for random
        await msg.add_reaction("✅")
        if captain == False:
            await msg.add_reaction("🌀")
            await msg.add_reaction("❌")
        reaction = await GetReaction(msg, 2, 180, ctx)
        if reaction == 1:
            await msg.clear_reactions()
            return 1
            
        if (reaction[0].emoji == "✅"):
            break
        if (reaction[0].emoji == "🌀"):
            await msg.clear_reactions()
            await msg.edit(content="Regenerating")
            for i in range(len(Attackers)-1, -1, -1):
                WaitingRoomMembers.append(Attackers[i])
                Attackers.pop(i)
            for i in range(len(Defenders)-1, -1, -1):
                WaitingRoomMembers.append(Defenders[i])
                Defenders.pop(i)                
            DividedWaitingRoom = [[],[],[],[],[],[],[],[],[]]
            for member in WaitingRoomMembers:
                Role = await FindRole(member)
                DividedWaitingRoom[Role].append(member)
            for i in range(len(DividedWaitingRoom)):
                if len(DividedWaitingRoom[i]) != 0:
                    random.shuffle(DividedWaitingRoom[i])
            SortedWaitingRoom = list(chain.from_iterable(DividedWaitingRoom))
            State = random.choice([True, False])
            if State:
                Attackers.append(SortedWaitingRoom[0])
                SortedWaitingRoom.pop(0)
                State = not State
            else:
                Defenders.append(SortedWaitingRoom[0])
                SortedWaitingRoom.pop(0)
                State = not State
            while len(SortedWaitingRoom) != 0:
                if State:
                    Attackers.append(SortedWaitingRoom[0])
                    SortedWaitingRoom.pop(0)
                    if len(SortedWaitingRoom) != 0:
                        Attackers.append(SortedWaitingRoom[0])
                        SortedWaitingRoom.pop(0)
                    State = not State
                else:
                    Defenders.append(SortedWaitingRoom[0])
                    SortedWaitingRoom.pop(0)
                    if len(SortedWaitingRoom) != 0:
                        Defenders.append(SortedWaitingRoom[0])
                        SortedWaitingRoom.pop(0)
                    State = not State
            WaitingRoomMembers = []
            Rand = random.choice(range(2))
            State = random.choice([True, False])
            await MakeSelection(Attackers, Defenders, WaitingRoomMembers, Rand, State, msg, ctx)
            
            
    await msg.clear_reactions()
    
    Category = await guild.create_category(CategoryTitle)
    AVC = await Category.create_voice_channel("Attackers")
    DVC = await Category.create_voice_channel("Defenders")
    for attacker in Attackers:
        await attacker.move_to(AVC)
    for defender in Defenders:
        await defender.move_to(DVC)
    
    await msg.add_reaction("🛑")
    while 1:
        await GetReaction(msg, 2, 0, ctx)
        conf = await ctx.channel.send("You are ending the match created by: " + ctx.author.name + "\nConfirm?")
        await conf.add_reaction("✅")
        await conf.add_reaction("🚫")
        reaction = await GetReaction(conf, 2, 180, ctx)
        if reaction[0].emoji == "✅":
            await conf.delete()
            break
        else:
            await conf.delete()
            
    for attacker in Attackers:
        try:
            await attacker.move_to(discord.utils.get(guild.voice_channels, name="Waiting Room"))
        except Exception:
            continue
    for defender in Defenders:
        try:
            await defender.move_to(discord.utils.get(guild.voice_channels, name="Waiting Room"))
        except Exception:
            continue
        
    await deletevc(ctx)
    
    return 0

@client.event
async def on_ready():
    print("Ready!\n-------")
    
@client.command()
async def start(context):
    try:
        global Instances
        guild = context.guild
        Instances += 1
        print("Current Instances =", Instances)
        
        msg1 = await context.channel.send("Starting 10 man queue. React to the check mark to confirm 10 players in the waiting room.")
        await msg1.add_reaction("✅")
        await msg1.add_reaction("❌")
        reaction = await GetReaction(msg1, 2, 180, context)
        await msg1.delete()
        if reaction == 1:
            Instances -= 1
            print("Current Instances =", Instances)
            return        
        
        WaitingRoom = discord.utils.get(guild.voice_channels, name="Waiting Room")
        WaitingRoomMembers = WaitingRoom.members
        
        if (len(WaitingRoom.members) > 10):
            await context.channel.send("Too many people in the Waiting Room. Using first 10 people to join.")
            WaitingRoomMembers = []
            for i in range(10):
                WaitingRoomMembers.append((WaitingRoom.members)[i])
        elif (len(WaitingRoom.members) < 2):
            await context.channel.send("Too few people in the Waiting Room")
            Instances -= 1
            print("Current Instances =", Instances)
            return
        elif (len(WaitingRoom.members)%2 != 0):
            await context.channel.send("Need even people in waiting room")
            Instances -= 1
            print("Current Instances =", Instances)
            return
       
        print("People in Waiting Room:")
        for VCmembers in WaitingRoomMembers:
            print(VCmembers.name)
        print("--------\n")
        
        msg2 = await context.channel.send("(C)aptains or (R)andom teams?")
        await msg2.add_reaction("🇨")
        await msg2.add_reaction("🇷")
        await msg2.add_reaction("❌")
        reaction = await GetReaction(msg2, 2, 180, context)
        await msg2.delete()
        if reaction == 1:
            Instances -= 1
            print("Current Instances =", Instances)
            return
           
        if (reaction[0].emoji == "🇨"):
            msg3 = await context.channel.send("(C)hoose captains or (R)andom captains?")
            await msg3.add_reaction("🇨")
            await msg3.add_reaction("🇷")
            await msg3.add_reaction("❌")
            reaction = await GetReaction(msg3, 2, 180, context)
            await msg3.delete()
            if reaction == 1:
                Instances -= 1
                print("Current Instances =", Instances)
                return
                
            if (reaction[0].emoji == "🇨"):
                msgCap = await context.channel.send("Select 2 Captains by reacting to the 🇨 below.")
                await msgCap.add_reaction("🇨")
                await msgCap.add_reaction("❌")
                reaction = await GetReaction(msgCap, 3, 180, context)
                if reaction == 1:
                    await msgCap.delete()
                    Instances -= 1
                    print("Current Instances =", Instances)
                    return
                captains = await reaction[0].users().flatten()
                if guild.name == "alone":
                    captains.remove(discord.utils.get(captains, name='Valorant 10 Mans dev version'))
                else:
                    captains.remove(discord.utils.get(captains, name='Valorant 10 Mans'))
                for captain in captains:
                    DelMember = discord.utils.get(WaitingRoomMembers, name=captain.name)
                    WaitingRoomMembers.remove(DelMember)
                await msgCap.delete()
                
            if (reaction[0].emoji == "🇷"):
                captains = []
                captain = random.choice(WaitingRoomMembers)
                captains.append(captain)
                WaitingRoomMembers.remove(captain)
                captain = random.choice(WaitingRoomMembers)
                captains.append(captain)
                WaitingRoomMembers.remove(captain)
                
            Rand1 = random.choice(range(2))
            Rand2 = random.choice(range(2))
            Attackers = []
            Defenders = []
            if (Rand1 == 0):
                Attackers.append(discord.utils.get(guild.members, name=captains[0].name))
                Defenders.append(discord.utils.get(guild.members, name=captains[1].name))
            else:
                Attackers.append(discord.utils.get(guild.members, name=captains[1].name))
                Defenders.append(discord.utils.get(guild.members, name=captains[0].name))
            
            msgPicks = await context.channel.send("Generating Picks")
            for i in range(len(WaitingRoomMembers)):
                await msgPicks.add_reaction(numArray[i])
            await msgPicks.add_reaction("❌")
            if (1==1): #change to 1 when full
                State = random.choice([True, False])
                returnVal = await MakeSelection(Attackers, Defenders, WaitingRoomMembers, Rand2, State, msgPicks, context)
                if returnVal == 1:
                    return
                while (len(WaitingRoomMembers) != 0):
                    State = not State
                    returnVal = await MakeSelection(Attackers, Defenders, WaitingRoomMembers, Rand2, State, msgPicks, context)
                    if returnVal == 1:
                        return
                    returnVal = await MakeSelection(Attackers, Defenders, WaitingRoomMembers, Rand2, State, msgPicks, context)
                    if returnVal == 1:
                        return
                        
            await ManageRoom(Attackers, Defenders, WaitingRoomMembers, msgPicks, context, True)
            
            
        elif (reaction[0].emoji == "🇷"):
            Attackers = []
            Defenders = []
            msgPicks = await context.channel.send("Generating Picks")
            DividedWaitingRoom = [[],[],[],[],[],[],[],[],[]]
            for member in WaitingRoomMembers:
                Role = await FindRole(member)
                DividedWaitingRoom[Role].append(member)
                print(member.name, " is rank ", Ranks[Role])
            for i in range(len(DividedWaitingRoom)):
                if len(DividedWaitingRoom[i]) != 0:
                    random.shuffle(DividedWaitingRoom[i])
            SortedWaitingRoom = list(chain.from_iterable(DividedWaitingRoom))
            State = random.choice([True, False])
            if State:
                Attackers.append(SortedWaitingRoom[0])
                SortedWaitingRoom.pop(0)
                State = not State
            else:
                Defenders.append(SortedWaitingRoom[0])
                SortedWaitingRoom.pop(0)
                State = not State
            while len(SortedWaitingRoom) != 0:
                if State:
                    Attackers.append(SortedWaitingRoom[0])
                    SortedWaitingRoom.pop(0)
                    if len(SortedWaitingRoom) != 0:
                        Attackers.append(SortedWaitingRoom[0])
                        SortedWaitingRoom.pop(0)
                    State = not State
                else:
                    Defenders.append(SortedWaitingRoom[0])
                    SortedWaitingRoom.pop(0)
                    if len(SortedWaitingRoom) != 0:
                        Defenders.append(SortedWaitingRoom[0])
                        SortedWaitingRoom.pop(0)
                    State = not State
            WaitingRoomMembers = []
            Rand = random.choice(range(2))
            State = random.choice([True, False])
            returnVal = await MakeSelection(Attackers, Defenders, WaitingRoomMembers, Rand, State, msgPicks, context)
            if returnVal == 1:
                return
            await ManageRoom(Attackers, Defenders, WaitingRoomMembers, msgPicks, context, False)
            
 
    except asyncio.TimeoutError:
        await context.channel.send("Timeout.")
        Instances -= 1
        print("Current Instances =", Instances)
        return
    except Exception:
        Instances -= 1
        print("Current Instances =", Instances)
        await context.channel.send("Some error occured.")
        return
    Instances -= 1
    print("Current Instances =", Instances)

@client.command()
async def deleteVC(context, arg):
    guild = context.guild
    
    Name = "Match Created by: " + arg
    Category = discord.utils.get(guild.categories, name=Name)
    
    if Category == None:
        await context.channel.send("That channel was not found.")
        return
    
    for i in range(1, -1, -1):
        await (Category.voice_channels)[i].delete()
        
    await Category.delete()
    
    return
    
@client.command()
async def map(context):
    randMap = random.choice(Maps)
    await context.channel.send("The randomly generated map is: " + randMap)
    return

@client.command()
async def side(context):
    randSide = random.choice(["Attackers", "Defenders"])
    await context.channel.send("The randomly generated side is: " + randSide)
    return

@client.command()
async def excuses(context):
    await context.channel.send(context.author.name + " wants you to stop making excuses!")

client.run(TOKEN)
