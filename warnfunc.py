import discord
import json
from asyncio import sleep
import datetime

def store(file, key=None, read=False, val=None):
	with open(file, 'r') as v:
		x = json.load(v)
	if read is not False:
		if key is None:
			return x
		else:
			return x[key]
	else:
		x[key] = val
		with open(file, 'w') as v:
			json.dump(x, v, indent=4)

async def strike(ctx):
	e = discord.Embed(title="KingShanes Epic Server STRIKES", description="These are strikes you get for breaking rules.", color=discord.Color.dark_blue())
	e.add_field(name="3 Warns:", value="1 Hour Mute", inline=False)
	e.add_field(name="6 Warns:", value="1 Week **BAN**", inline=False)
	e.add_field(name="9 Warns:", value="***PERM BAN***", inline=False)
	e.set_footer(text="React to this message to gain access")
	msg = await ctx.send(embed=e)
	await msg.add_reaction('✅')
	store('config.json', 'mid', False, str(msg.id))

async def rules(ctx):
	await ctx.message.delete()
	e = discord.Embed(title="KingShanes Epic Server RULES", description="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\nThe **server rules** can be found below. Breaking these rules **can result in a punishment**. Not all rules are listed here, **so use your common sense.**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬", color=discord.Color.dark_green(), timestamp=datetime.datetime.utcnow())
	e.set_footer(text="Have fun in KingShanes Epic Server! Updated")
	e.add_field(name="1. Channels", value="Please use each channel for its intentional purpose.", inline=False)
	e.add_field(name="2. DM Rules:", value="No DMing members of the server with your invite links, as this will result in an immediate ban. Rules still apply in DMs!", inline=False)
	e.add_field(name="3. Moderator Rules:", value="If you have a problem with one of our moderator's decisions, please DM an Admin, as they can sort out your situation. Please do not ping moderators unnecessarily, as you will be kicked.", inline=False)
	e.add_field(name="4. No Begging", value="Begging for Discord Nitro, roles, in-game/server currency, money, or anything is not allowed.", inline=False)
	e.add_field(name="5. Content Rules", value="**No personal information of yourself or others**, and this will result in a kick or ban. No sexually explicit content/NSFW/pornagraphy, as this will result in a ban. No illegal/piracy-related content is allowed, and punishment is up to a moderator. No \"Hard R's\". Don't ghost tag people. **Don't take jokes too far**. Moderators reserve the right to delete and edit posts.", inline=False)
	e.add_field(name="6. Content Rules (pt. 2)", value="No **harassment, personal attacks/threats, sexism, racism, hate speech, offensive language, or discussions related to politics, religion, or sexual discussions**. Punishment is up to moderators. Cursing is allowed, but please keep it to a minimum.", inline=False)
	e.add_field(name="7. Spam", value="No spam or text walls are allowed, and will result in a kick, or another punishment decided by a moderator. Some trolling is allowed, but up to a certain point. No excessive messaging (breaking up an idea in many posts instead of writing all out in one post).", inline=False)
	e.add_field(name="9. Advertisement", value="Advertisement is not allowed in any channel except when it says specifically in the description.", inline=False)
	e.add_field(name="10. Links", value="No shady links or links that redirect. This will result in a mute.", inline=False)
	e.add_field(name="11. Voice channel rules:", value="No voice channel hopping. No annoying, loud or high pitch noises. Moderators reserve the right to disconnect, mute, deafen, or move members out of and into voice channels.", inline=False)
	e.add_field(name="12. Follow TOS", value="You must follow the [Discord TOS](https://discord.com/terms). These rules should be followed all times.", inline=False)
	await ctx.send(embed=e)
	await strike(ctx)

async def appendWarn(msg, member, message):
	x = store('warns.json', key=None, read=True)
	if str(member.id) not in x:
		x[str(member.id)] = {}
		x[str(member.id)]['one'] = True
		x[str(member.id)]['oner'] = message
		x[str(member.id)]['two'] = None
		x[str(member.id)]['twor'] = None
		x[str(member.id)]['three'] = None
		x[str(member.id)]['threer'] = None
		x[str(member.id)]['four'] = None
		x[str(member.id)]['fourr'] = None
		with open('warns.json', 'w') as v:
			json.dump(x, v, indent=4)
	else:
		if x[str(member.id)]['one'] is True:
			if x[str(member.id)]['two'] is True and x[str(member.id)]['three'] is not True:
				x[str(member.id)]['three'] = True
				x[str(member.id)]['threer'] = message
				with open('warns.json', 'w') as v:
					json.dump(x, v, indent=4)
			elif x[str(member.id)]['three'] is True and x[str(member.id)]['four'] is not True:
				x[str(member.id)]['four'] = True
				x[str(member.id)]['fourr'] = message
				await msg.channel.send(f"{member.mention}! You have too many warnings! You will be banned if you do it again.") 
				with open('warns.json', 'w') as v:
					json.dump(x, v, indent=4)
			else:
				x[str(member.id)]['two'] = True
				x[str(member.id)]['twor'] = message
				with open('warns.json', 'w') as v:
					json.dump(x, v, indent=4)
		elif x[str(member.id)]['one'] is not True:
			x[str(member.id)]['one'] = True
			x[str(member.id)]['oner'] = message
			with open('warns.json', 'w') as v:
				json.dump(x, v, indent=4)
		else:
			await msg.channel.send("Unknown Erorr")

async def deletewarn(ctx, member, nub):
	x = store('warns.json', key=None, read=True)
	if str(member.id) not in x:
		e = discord.Embed(f"No warn data found for user {member.name}", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
		await ctx.send(embed=e)
		return
	if nub == 1:
		nub = 'one'
		nubr = 'oner'
	elif nub == 2:
		nub = 'two'
		nubr = 'twor'
	elif nub == 3:
		nub = 'three'
		nubr = 'threer'
	else:
		nub = 'four'
		nubr = 'fourr'
	x[str(member.id)][nub] = None
	x[str(member.id)][nubr] = None
	with open('warns.json', 'w') as v:
		json.dump(x, v, indent=4)

async def getWarns(ctx, member):
	if member is None:
		member = ctx.author
	await ctx.message.delete()
	x = store('warns.json', key=None, read=True)
	if not str(member.id) in x:
		e = discord.Embed(title=f'No warn data for user {member.name}', color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
		await ctx.send(embed=e)
		return
	def desc():
		if x[str(member.id)]['one'] is None:
			return 'No warnings for this user'
		else:
			return 'Shows all warnings for this user'
	def colr():
		if x[str(member.id)]['one'] is None:
			return discord.Color.blue()
		elif x[str(member.id)]['two'] is None:
			return discord.Color.green()
		elif x[str(member.id)]['three'] is None:
			return discord.Color.orange()
		elif x[str(member.id)]['four'] is None:
			return discord.Color.red()
		else:
			return discord.Color.purple()
	e = discord.Embed(title=f'Warns for user {member.name}', description=desc(), color=colr(), timestamp=datetime.datetime.utcnow())
	if x[str(member.id)]['one'] is not None:
		e.add_field(name='Warning 1', value=f"Status: {x[str(member.id)]['one']}\nReason: {x[str(member.id)]['oner']}", inline=False)
	if x[str(member.id)]['two'] is not None:
		e.add_field(name='Warning 2', value=f"Status: {x[str(member.id)]['two']}\nReason: {x[str(member.id)]['twor']}", inline=False)
	if x[str(member.id)]['three'] is not None:
		e.add_field(name='Warning 3', value=f"Status: {x[str(member.id)]['three']}\nReason: {x[str(member.id)]['threer']}", inline=False)
	if x[str(member.id)]['four'] is not None:
		e.add_field(name='Warning 4', value=f"Status: {x[str(member.id)]['four']}\nReason: {x[str(member.id)]['fourr']}", inline=False)

	await ctx.send(embed=e)
