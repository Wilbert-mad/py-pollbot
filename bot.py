import discord

from discord.ext import commands

client = commands.Bot(command_prefix='p!')
emojis = [None, '1️⃣', '2️⃣', '3️⃣', '4️⃣',
          '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']


@client.event
async def on_ready():
    print('ready')


def capital(message: str) -> str:
    mark = '?' if not message.endswith('?') else ''
    return f"{message[0].upper()}{message[:0:-1][::-1]}{mark}"


def add_number(choices: list) -> list:
    choices = choices[::-1]
    numbered = []
    for choice in choices:
        numbered.append(f"{emojis[choices.index(choice)+1]} {choice}")

    return numbered


@client.command(name='poll', brief='create a channel poll', usage='<question> [...choices]')
async def _poll(ctx, *args):
    if len(args) <= 0:
        return await ctx.send('No poll question set!')

    question: str = args[0]
    choices: list = None

    if len(args) > 1:
        choices = []
        for I in args[:0:-1]:
            choices.append(I)

    embed = discord.Embed()
    reaction_responces = add_number(choices) if choices != None else [
        '1️⃣ Yes', '2️⃣ No']

    next_line = "\n"
    embed.title = 'Poll'
    embed.color = discord.colour.Color.random()
    embed.description = f'{capital(question)}\n{next_line.join(reaction_responces)}'

    msg = await ctx.send(embed=embed)

    if choices == None:
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
    else:
        for ops in choices:
            position = choices.index(ops)+1
            await msg.add_reaction(emojis[position])
