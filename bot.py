import discord, aiohttp, asyncio, datetime
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import bot

intents = discord.Intents.all()
client = commands.Bot(command_prefix='>', intents=intents, case_insensitive=True, chunk_guilds_at_startup=False)
#chunk_guilds_at_startup is for not saving guilds datas in the cache (less ram consumption)
#case_insensitive is for using command with full caps for exemple

tree = client.tree #for slash commands

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await client.tree.sync()
    await update_stats()

async def update_stats():
    while True:
        total_members = sum(guild.member_count for guild in client.guilds)
        activity_text = f"In {len(client.guilds)} servers | Serving {total_members} members"
        await client.change_presence(activity=discord.Game(name=activity_text))
        await asyncio.sleep(360)
        

#generating embed
generating_embed = discord.Embed(
        title="Generating Image",
        description="Image Is Generating, It takes 30 ~ 50 seconds to generate",
        color=discord.Color.orange())


#define the api header
async def head(prompt, image_format, model):
    width , height = map(int, image_format.split("x"))
    api_key = ""#change by your api key on the bot from visioncraft : https://t.me/VisionCraft_bot (use the command /key)
    data = {
        "model": model,
        "prompt": prompt,
        "token": api_key,
        "width": width,
        "height": height
    }
    return data

#make the request to the api
async def generate_image(data) -> bytes:
    api_url = "https://visioncraft.top"
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_url}/sd", json=data) as response:
            image = await response.read()
            return image

#upload the image on a file host
async def telegraph_file_upload(file_bytes):
    url = 'https://telegra.ph/upload'
    try:
        data = aiohttp.FormData()
        data.add_field('file', file_bytes, filename='image.png', content_type='image/png')

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                response_data = await response.json()
                if response.status == 200 and response_data and isinstance(response_data, list) and 'src' in response_data[0]:
                    telegraph_url = response_data[0]['src']
                    full_url = f'https://telegra.ph{telegraph_url}'
                    return full_url
                else:
                    print(f'Unexpected response data or status: {response_data}, Status: {response.status}')
                    return None
    except Exception as e:
        print(f'Error uploading file to Telegraph: {str(e)}')
        return None

#simple command
@client.command()
async def imagine(ctx, *, prompt: str):
    message = await ctx.send(embed=generating_embed)

    data = await head(prompt, image_format="1024x1024", model="RealVisXLV40Turbo-40")
    image = await generate_image(data)
    telegraph_url = await telegraph_file_upload(image)

    if telegraph_url:
        image_embed = discord.Embed(title="Generated Image", color=discord.Color.blue())
        image_embed.set_image(url=telegraph_url)

        await message.edit(content=None, embed=image_embed)
        print(f"Image URL: {telegraph_url}")  # Log the image URL to the console
    else:
        await message.edit(content="Failed to upload image.", embed=None)

    

#slash command
@tree.command(description="generate images by ai")
@app_commands.describe(prompt="description of the image", private="make the image visble for you or everyone", image_format="the format of the image", image_type="type of the image like anime, 3d, etc...")
@app_commands.choices(
    image_format = [
    app_commands.Choice(name="default・Square", value="1024x1024"),
    app_commands.Choice(name="Portrait", value="768x1024"),
    app_commands.Choice(name="Landscape", value="1024x768"),
],
    private = [
    app_commands.Choice(name="True", value="True"),
    app_commands.Choice(name="False", value="False"),
    ],
    image_type = [
        app_commands.Choice(name="default・realistic", value="RealVisXLV40Turbo-40"),
        app_commands.Choice(name="3D", value="UnrealXL-v1"),
        app_commands.Choice(name="anime", value="AnimefromHaDeS-v16HQ"),
    ]
)
async def imagine(ctx : discord.Interaction, prompt: str, image_format: app_commands.Choice[str] = None, image_type: app_commands.Choice[str] = None, private: app_commands.Choice[str] = None):
    private_value = True if private is not None and private.value == "True" else False 
    img_format = image_format.value if image_format is not None else "1024x1024"
    model = image_type.value if image_type is not None else "RealVisXLV40Turbo-40"
    
    await ctx.response.send_message(embed=generating_embed, ephemeral=bool(private_value))
    

    data = await head(prompt, img_format, model)
    image = await generate_image(data)
    telegraph_url = await telegraph_file_upload(image)
    
    if telegraph_url:
        image_embed = discord.Embed(title="Generated Image", color=discord.Color.blue())
        image_embed.set_image(url=telegraph_url)
        print(f"Image URL: {telegraph_url}")
        await ctx.edit_original_response(content=None, embed=image_embed)
        
        
    else:
        await ctx.edit_original_response(content="Failed to upload image.", embed=None)


    
client.run("")#use your bot token
