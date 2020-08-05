import discord
import io
from lobsterize import lobsterize
from router import Router
import aiohttp
import asyncio
import concurrent.futures
from functools import partial

client = discord.Client()
token = 'NzM2NTQxODEzOTY3NTUyNTMz.XxwUBA.6SZ6ndtnpY0dY435CrRp0T69FgM'
router = Router(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        command, prefix = router.resolve(message.content)
        await command(message, prefix)
    except ValueError:
        pass

@router.route('lobster ', 'l ')
@router.description('ordinary lobster')
async def on_lobster(message, prefix: str, wide=False):
    content = message.content
    if message.attachments:
        text = content[len(prefix):].strip()
        attachment = message.attachments[0]
        image = await attachment.read()
        format = attachment.filename.split('.')[-1].lower()
        loop = asyncio.get_running_loop()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            res_jpg = await loop.run_in_executor(pool, partial(lobsterize, io.BytesIO(image), text, format, wide=wide))
        with io.BytesIO(res_jpg) as res_jpg_file:
            out_file = discord.File(res_jpg_file, 'lobster.jpg')
            await message.channel.send(file=out_file)
    else:
        await message.channel.send('do you are have stupid, attach your picture')

@router.route('widelobster ', 'wl ')
@router.description('lobster, but text is bigger on wider images')
async def on_wide_lobster(message, prefix: str):
    return await on_lobster(message, prefix, wide=True)

@router.fallback
async def on_unknown_command(message, prefix: str):
    await message.channel.send("unknown command, maybe try 'help' command?")

@router.route('help', 'h')
@router.description("I don't now, maybe 'help' will play 'All Star' by Smath Mouth")
async def on_help(message, prefix: str):
    await message.channel.send(router.generate_help())

@router.route('allstar')
@router.description('...')
async def on_all_star(message, prefix: str):
    text = 'https://open.spotify.com/track/3cfOd4CMv2snFaKAnMdnvK?si=UrNGFWRpSxyhK338gJDnVg'
    await message.channel.send(text)

@router.route('ip')
@router.description("IP Address of the server (but why do I need it)")
async def on_ip(message, prefix: str):
    API_ENDPOINT = 'https://api.ipify.org'
    async with aiohttp.ClientSession() as session:
        async with session.get(API_ENDPOINT, params={'format': 'json'}) as resp:
            json = await resp.json()
            await message.channel.send(f'Server IP: {json["ip"]}')

client.run(token)
