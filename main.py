import os
import asyncio
import random
from itertools import chain

numArray = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

numDict = {"1️⃣": 0, "2️⃣": 1, "3️⃣": 2, "4️⃣": 3, "5️⃣": 4, "6️⃣": 5, "7️⃣": 6, "8️⃣": 7}

Maps = ["Bind", "Haven", "Ascent", "Icebox"]

Ranks = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Immortal", "Radiant", "Unranked"]

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand
from leaderboard import Leaderboard, loadData

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix="v!")
slash = SlashCommand(client, sync_commands=False)
Instances = 0
WaitingRoomQueue = {}

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
			elif (reaction[0].emoji == "❌") and (reaction[1].name != client.user.name):
				await ctx.channel.send("Exited.")
				return 1
			elif (reaction[0].count >= arg):
				break
		else:
			if (reaction[0].message != msg):
				continue
			elif (reaction[0].emoji == "❌") and (reaction[1].name == client.user.name):
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
			MessageStr += member.name + "#" + member.discriminator + "\n"
		MessageStr += "\nDefenders:\n"
		for member in Defenders:
			MessageStr += member.name + "#" + member.discriminator + "\n"
		await msg.edit(content=MessageStr)
		return

	if bool(a)^bool(b):
		MessageStr = "---------------------\n**Attacker's pick (captain only):**\n\n"
		MessageStr += "Availible picks:\n"
		for i in range(len(WaitingRoomMembers)):
			MessageStr += numArray[i] + ":   " + WaitingRoomMembers[i].name + "#" + WaitingRoomMembers[i].discriminator + "\n"
		MessageStr += "\nAttackers:\n"
		for member in Attackers:
			MessageStr += member.name + "#" + member.discriminator + "\n"
		MessageStr += "\nDefenders:\n"
		for member in Defenders:
			MessageStr += member.name + "#" + member.discriminator + "\n"
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
			MessageStr += numArray[i] + ":   " + WaitingRoomMembers[i].name + "#" + WaitingRoomMembers[i].discriminator + "\n"
		MessageStr += "\nAttackers:\n"
		for member in Attackers:
			MessageStr += member.name + "#" + member.discriminator + "\n"
		MessageStr += "\nDefenders:\n"
		for member in Defenders:
			MessageStr += member.name + "#" + member.discriminator + "\n"
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

async def MakeRandomSelections(Attackers, Defenders, WaitingRoomMembers):
	DividedWaitingRoom = [[],[],[],[],[],[],[],[],[]]
	for member in WaitingRoomMembers:
		Role = await FindRole(member)
		DividedWaitingRoom[Role].append(member)
	for i in range(len(DividedWaitingRoom)):
		if len(DividedWaitingRoom[i]) != 0:
			random.shuffle(DividedWaitingRoom[i])
	SortedWaitingRoom = list(chain.from_iterable(DividedWaitingRoom))
	State = random.choice([True, False])
	if len(SortedWaitingRoom) == 2:
		if State:
			Attackers.append(SortedWaitingRoom[0])
			Defenders.append(SortedWaitingRoom[1])
		else:
			Attackers.append(SortedWaitingRoom[1])
			Defenders.append(SortedWaitingRoom[0])
		return
	if State:
		Attackers.append(SortedWaitingRoom[0])
		Attackers.append(SortedWaitingRoom[len(SortedWaitingRoom)-1])
		SortedWaitingRoom.pop(0)
		SortedWaitingRoom.pop(len(SortedWaitingRoom)-1)
		State = not State
	else:
		Defenders.append(SortedWaitingRoom[0])
		Defenders.append(SortedWaitingRoom[len(SortedWaitingRoom)-1])
		SortedWaitingRoom.pop(0)
		SortedWaitingRoom.pop(len(SortedWaitingRoom)-1)
		State = not State
	while len(SortedWaitingRoom) != 2:
		if State:
			Attackers.append(SortedWaitingRoom[0])
			Attackers.append(SortedWaitingRoom[len(SortedWaitingRoom)-1])
			SortedWaitingRoom.pop(0)
			SortedWaitingRoom.pop(len(SortedWaitingRoom)-1)
			if len(SortedWaitingRoom) != 2:
				Attackers.append(SortedWaitingRoom[0])
				Attackers.append(SortedWaitingRoom[len(SortedWaitingRoom)-1])
				SortedWaitingRoom.pop(0)
				SortedWaitingRoom.pop(len(SortedWaitingRoom)-1)
			State = not State
		else:
			Defenders.append(SortedWaitingRoom[0])
			Defenders.append(SortedWaitingRoom[len(SortedWaitingRoom)-1])
			SortedWaitingRoom.pop(0)
			SortedWaitingRoom.pop(len(SortedWaitingRoom)-1)
			if len(SortedWaitingRoom) != 2:
				Defenders.append(SortedWaitingRoom[0])
				Defenders.append(SortedWaitingRoom[len(SortedWaitingRoom)-1])
				SortedWaitingRoom.pop(0)
				SortedWaitingRoom.pop(len(SortedWaitingRoom)-1)
			State = not State
	State = random.choice([True, False])
	if len(Attackers) == len(Defenders):
		if State:
			Attackers.append(SortedWaitingRoom[0])
			SortedWaitingRoom.pop(0)
			Defenders.append(SortedWaitingRoom[0])
			SortedWaitingRoom.pop(0)
		else:
			Defenders.append(SortedWaitingRoom[0])
			SortedWaitingRoom.pop(0)
			Attackers.append(SortedWaitingRoom[0])
			SortedWaitingRoom.pop(0)
	elif len(Attackers) < len(Defenders):
		Attackers.append(SortedWaitingRoom[0])
		SortedWaitingRoom.pop(0)
		Attackers.append(SortedWaitingRoom[0])
		SortedWaitingRoom.pop(0)
	else:
		Defenders.append(SortedWaitingRoom[0])
		SortedWaitingRoom.pop(0)
		Defenders.append(SortedWaitingRoom[0])
		SortedWaitingRoom.pop(0)

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
			random.shuffle(WaitingRoomMembers)
			numPlayers = len(WaitingRoomMembers)
			for i in range(numPlayers//2):  
				Attackers.append(WaitingRoomMembers[0])
				WaitingRoomMembers.pop(0)
			for i in range(numPlayers//2):  
				Defenders.append(WaitingRoomMembers[0])
				WaitingRoomMembers.pop(0)
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
		stopr = await GetReaction(msg, 2, 0, ctx)
		conf = await ctx.channel.send("You are ending the match created by: " + ctx.author.name + "\nReact 🇦 if the attackers won,\n🇩 if the defenders won,\n👎 if a full game was not played,\nand 🚫 to cancel.")
		await conf.add_reaction("🇦")
		await conf.add_reaction("🇩")
		await conf.add_reaction("👎")
		await conf.add_reaction("🚫")
		reaction = await GetReaction(conf, stopr[1], 180, ctx)
		if reaction[0].emoji == "🇦":
			winStr = []
			lossStr = []
			for attacker in Attackers:
				winStr.append(attacker.name + "#" + attacker.discriminator)
			for defender in Defenders:
				lossStr.append(defender.name + "#" + defender.discriminator)
			print(winStr, lossStr)
			data = loadData()
			data.update(winStr, lossStr, str(guild.id))
			data.getArray(str(guild.id))
			data.save()
			await conf.delete()
			await ctx.channel.send("Attackers win!")
			break
		elif reaction[0].emoji == "🇩":
			winStr = []
			lossStr = []
			for defender in Defenders:
				winStr.append(defender.name + "#" + defender.discriminator)
			for attacker in Attackers:
				lossStr.append(attacker.name + "#" + attacker.discriminator)
			print(winStr, lossStr)
			data = loadData()
			data.update(winStr, lossStr, str(guild.id))
			data.getArray(str(guild.id))
			data.save()
			await conf.delete()
			await ctx.channel.send("Defenders win!")
			break
		elif reaction[0].emoji == "👎":
			await conf.delete()
			break
		else:
			await conf.delete()		
	await msg.clear_reactions()

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
	global WaitingRoomQueue
	guilds = client.guilds
	for guild in guilds:
		WaitingRoomQueue[str(guild.id)] = []
		WR = discord.utils.get(guild.voice_channels, name="Waiting Room")
		for member in WR.members:
			WaitingRoomQueue[str(guild.id)].append(member)
	print("Ready!\n-------")
	
@client.event
async def on_voice_state_update(member, before, after):
	global WaitingRoomQueue
	try:
		if ((before.channel == None) or (before.channel.name != "Waiting Room")) and(after.channel.name == "Waiting Room"):
			WaitingRoomQueue[str(member.guild.id)].append(member)
	except AttributeError:
		pass
	try:
		if ((after.channel == None) or (after.channel.name != "Waiting Room")) and (before.channel.name == "Waiting Room"):
			WaitingRoomQueue[str(member.guild.id)].remove(member)
	except AttributeError:
		pass
	except ValueError:
		pass
	# print("Waiting Room Members in " + member.guild.name + " server:")
	# for qmember in WaitingRoomQueue[str(member.guild.id)]:
		# print(qmember.name, end=" ")
	# print()
	# print(member)
	
@client.event
async def on_guild_join(guild):
	global WaitingRoomQueue
	WaitingRoomQueue[str(guild.id)] = []
	WR = discord.utils.get(guild.voice_channels, name="Waiting Room")
	for member in WR.members:
		WaitingRoomQueue[str(guild.id)].append(member)
	print(guild.name + " joined by Valorant 10 mans!")

@client.event	
async def on_guild_remove(guild):
	global WaitingRoomQueue
	del WaitingRoomQueue[str(guild.id)]
	print("Valorant 10 mans left \"" + guild.name + "\" server")
	
@slash.slash(description="Starts 10 man game.")
#@client.command()
async def start(context):
	await context.send("Starting 10 man queue.")
	try:
		global Instances
		global WaitingRoomQueue
		guild = context.guild
		Instances += 1
		print("Current Instances =", Instances)
		
		msg1 = await context.channel.send("React to the check mark to confirm 10 players in the waiting room.")
		await msg1.add_reaction("✅")
		await msg1.add_reaction("❌")
		reaction = await GetReaction(msg1, 2, 180, context)
		await msg1.delete()
		if reaction == 1:
			Instances -= 1
			print("Current Instances =", Instances)
			return		
		
		WaitingRoom = discord.utils.get(guild.voice_channels, name="Waiting Room")
		WaitingRoomMembers = WaitingRoomQueue[str(guild.id)][0:10]
		
		if (len(WaitingRoom.members) > 10):
			await context.channel.send("Too many people in the Waiting Room. Using first 10 people to join.")
		elif (len(WaitingRoomMembers) < 2):
			await context.channel.send("Too few people in the Waiting Room.")
			Instances -= 1
			print("Current Instances =", Instances)
			return
		elif (len(WaitingRoomMembers)%2 != 0):
			await context.channel.send("Need even people in waiting room.")
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
				captains.remove(discord.utils.get(captains, name=client.user.name))
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
			await MakeRandomSelections(Attackers, Defenders, WaitingRoomMembers)
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

@slash.slash(description="Use this to remove yourself from queue but stay in the Waiting Room.")
async def removemefromq(context):
	guild = context.guild
	global WaitingRoomQueue
	guildId = str(guild.id)
	CurrentQueue = WaitingRoomQueue[guildId]
	if (context.author.guild == guild) and (context.author.voice.channel.name == "Waiting Room"):
		CurrentQueue.remove(context.author)
		await context.send("Successfully Removed " + context.author.name + " from the queue. You will have to leave then join the waiting room to rejoin queue.")
	else:
		await context.send("Could not find " + context.author.name + " in the queue.")


@slash.slash(description="Display the top 10 leaderboard for who has played the most games so far!")
async def leaderboard(context):
	data = loadData()
	leaders = data.getArray(str(context.guild.id))
	
	if (len(leaders) == 0):
		await context.send("No matches in the history!")
		return
	await context.send("Displaying top 10 players:")
	displayStr = ""
	index = 1
	for members in leaders:
		if len(members) == 1:
			displayStr += str(index) + ":\n\t" + members[0][0] + "\n\tGame count of " + str(members[0][1]) + " and win count of " + str(members[0][2]) + "\n"
			index += 1
		elif len(members) == 2:
			displayStr += "Tied for " + str(index) + ":\n\t" + members[0][0] + " and " + members [1][0] + "\n\tGame count of " + str(members[0][1]) + " and win count of " + str(members[0][2]) + "\n"
			index += 2
		else:
			displayStr += "Tied for " + str(index) + ":\n\t"
			for i in range(len(members) - 1):
				displayStr += members[i][0] + ", "
			displayStr += "and " + members[len(members)-1][0]
			displayStr += "\n\tGame count of " + str(members[0][1]) + " and win count of " + str(members[0][2]) + "\n"
			index += len(members)
	await context.channel.send(displayStr)


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
	
@slash.slash(description="Generates a random map from the Valorant map pool.")
async def map(context):
	randMap = random.choice(Maps)
	await context.send("The randomly generated map is: " + randMap)
	return

@client.command()
async def side(context):
	randSide = random.choice(["Attackers", "Defenders"])
	await context.channel.send("The randomly generated side is: " + randSide)
	return

@client.command()
async def excuses(context):
	await context.channel.send(context.author.name + " wants you to stop making excuses!")

@client.command()
async def printdata(context):
	data = loadData()
	data.printData()
@client.command()
async def printarray(context):
	data = loadData()
	print(data.getArray(str(context.guild.id)))

client.run(TOKEN)
