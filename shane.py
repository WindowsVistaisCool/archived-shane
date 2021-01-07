import discord
from discord.ext import commands
import json
import datetime
import warnfunc
from asyncio import sleep

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

client = commands.Bot(command_prefix='/')
client.remove_command('help')

@client.event
async def on_ready():
	print("ready")
	x = store('config.json', 'ver', True)
	ver = x['vers']
	def vrt():
		if x['type'] == 'full':
			return 'FLL RL'
		elif x['type'] == 'bug':
			return 'BUG FX'
		else:
			return 'OTHR FX'
	vert = vrt()
	def stat():
		if x['type'] == 'full':
			return discord.Status.online
		elif x['type'] == 'bug':
			return discord.Status.idle
		else:
			return discord.Status.dnd
			
	await client.change_presence(status=stat(), activity=discord.Activity(type=discord.ActivityType.watching, name=f'version {ver} ({vert})'))

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send("Permission Error...")
		await ctx.send("Sudo Required, this will go in the logs for the administrator to review.")
	print(error)

@client.event
async def on_raw_reaction_add(payload):
	x = store('config.json', 'mid', True)
	z = store('config.json', 'rroles', True)
	zt = store('config.json', 'rrolesrole', True)
	if payload.message_id == int(x):
		if payload.emoji.name == "✅":
			guild = client.get_guild(payload.guild_id)
			role = guild.get_role(778339911643955270)
			await payload.member.add_roles(role)
	if str(payload.message_id) in z:
		for msg in z:
			if str(payload.message_id) == msg:
				if payload.emoji.name == "✅":
					guild = client.get_guild(payload.guild_id)
					role = guild.get_role(int(zt[msg]))
					await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
	x = store('config.json', None, True)
	if str(payload.message_id) in x['rroles']:
		for msg in x['rroles']:
			if str(payload.message_id) == msg:
				if payload.emoji.name == "✅":
					guild = client.get_guild(payload.guild_id)
					member = await guild.fetch_member(payload.user_id)
					role = guild.get_role(int(x['rrolesrole'][msg]))
					await member.remove_roles(role)

@client.group()
async def rr(ctx):
	if ctx.invoked_subcommand is None:
		await ctx.send("Invalid reaction role subcommand passed.")

@rr.command()
@commands.is_owner()
async def add(ctx, messageid, roleid):
	await ctx.message.delete()
	x = store('config.json', None, True)
	x['rroles'][messageid] = "PLACEHOLDER"
	x['rrolesrole'][messageid] = roleid
	with open('config.json', 'w') as v:
		json.dump(x, v, indent=4)
	msg = await ctx.channel.fetch_message(int(messageid))
	await msg.add_reaction("✅")
	m2 = await ctx.send("Reaction role added")
	await sleep(1)
	await m2.delete() 

@rr.command()
@commands.is_owner()
async def delete(ctx, messageid):
	await ctx.message.delete()
	x = store('config.json', None, True)
	x["rroles"].pop(messageid)
	x["rrolesrole"].pop(messageid)
	with open('config.json', 'w') as v:
		json.dump(x, v, indent=4)
	m2 = await ctx.send("Reaction role removed")
	await sleep(1)
	await m2.delete() 
	
@client.command()
@commands.is_owner()
async def sysout(ctx, ms):
	print(ms)
	await ctx.send("Console Log added")
	
@client.command()
async def help(ctx):
	x = store('config.json', 'help', read=True)
	e = discord.Embed(title='Help for Shane Utilities', description="**<>** Fields are optional. **{}** Fields are manditory.", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
	nu = 0
	for help in x:
		nu += 1
		e.add_field(name=x[str(nu)]["com"], value=x[str(nu)]["desc"], inline=False)
	await ctx.send(embed=e)

@client.command()
@commands.is_owner()
async def say(ctx, times):
	await ctx.message.delete()
	for x in range(int(times)):
		message = input("Message: ")
		if message.startswith('/embed'):
			print("Embed setup starting...")
			etitle = input("Embed title: ")
			e = discord.Embed(title=etitle, color=discord.Color.blurple())
			await ctx.send(embed=e)
		else:
			await ctx.send(message)
		
@client.event
async def on_message(ctx):
	if ctx.author.bot:
		return
	# Filter
	if ('n' + 'i' + 'gg' + 'e' + 'r') in ctx.content.lower():
		await ctx.delete()
		await warnfunc.appendWarn(ctx, ctx.author, '\'N Word\'')
		await warnfunc.appendWarn(ctx, ctx.author, '\'N Word\'')
		await ctx.channel.send(f'{ctx.author.mention}, rule 1! 2 warnings were added.')
	elif 'shitass' in ctx.content.lower():
		await ctx.channel.send(f'Did someone say `shitass`?')
		await ctx.channel.send(file=discord.File('shitass.png'))
	elif '<@!392502213341216769>' in ctx.content.lower():
		if ctx.author.id != 392502213341216769:
			await ctx.channel.send("How dare you ping my owner! You little sh`*`t will pay for this!")

	await client.process_commands(ctx)

@client.command()
@commands.is_owner()
async def purge(ctx, amount):
	await ctx.message.delete()
	await ctx.channel.purge(limit=int(amount))
	
@client.command()
@commands.is_owner()
async def warn(ctx, member: discord.Member, *, message):
	await ctx.message.delete()
	await warnfunc.appendWarn(ctx.message, member, message)

@client.command()
@commands.is_owner()
async def delwarn(ctx, member: discord.Member, numb):
	await ctx.message.delete()
	await warnfunc.deletewarn(ctx, member, int(numb))

@client.command()
@commands.is_owner()
async def trackwarns(ctx, member: discord.Member):
	await ctx.message.delete()
	await warnfunc.appendWarn(ctx.message, member, "Track Start, will be deleted")
	await warnfunc.deletewarn(ctx, member, 1)
	e = discord.Embed(title=f"Started tracking warns for user {member.name}", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
	await ctx.send(embed=e)

@client.command()
@commands.is_owner()
async def untrackwarns(ctx, member: discord.Member):
	await ctx.message.delete()
	x = store('warns.json', key=None, read=True)
	x.pop(str(member.id))
	with open('warns.json', 'w') as v:
		json.dump(x, v, indent=4)
	e = discord.Embed(title=f"Stopped tracking warns for user {member.name}", color=discord.Color.blurple(), timestamp=datetime.datetime.utcnow())
	await ctx.send(embed=e)

@client.command()
async def warns(ctx, member: discord.Member=None):
	await warnfunc.getWarns(ctx, member)

@client.command()
@commands.is_owner()
async def ban(ctx, member: discord.Member=None, reason="stupid"):
	if member is None:
		member = ctx.author
	await member.ban(reason=reason)

@client.command()
@commands.is_owner()
async def rules(ctx):
	await warnfunc.rules(ctx)

@client.command()
@commands.is_owner()
async def strikes(ctx):
	await warnfunc.strike(ctx)

client.run(store('config.json', 'token', True))
