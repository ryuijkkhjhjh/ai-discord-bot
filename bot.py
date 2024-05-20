import discord, aiohttp, asyncio, datetime, re
from discord import ui, app_commands
from discord.ext import commands
from discord.ext.commands import bot

intents = discord.Intents.all()
client = commands.Bot(command_prefix='>', intents=intents, case_insensitive=True, chunk_guilds_at_startup=False)
#chunk_guilds_at_startup is for not saving guilds datas in the cache (less ram consumption)
#case_insensitive is for using command with full caps for exemple

tree = client.tree

start_time = datetime.datetime.now(datetime.timezone.utc)

async def generate_image(prompt, model, timeout=120):
    counter = 0
    api_url = "https://api.sitius.ir/"
    data = {
        "model": model,
        "prompt": prompt,
        "steps": 30,
        "cfg_scale": 7,
        "sampler" : "Euler",
        "negative_prompt": "canvas frame, cartoon, 3d, ((disfigured)), ((bad art)), ((deformed)), ((extra limbs)), ((close up)), ((b&w)), weird colors, blurry, (((duplicate))), ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), ((ugly)), (((bad proportions))), (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), (fused fingers), (too many fingers), (((long neck))), Photoshop, video game, tiling, poorly drawn feet, body out of frame, nsfw"
    }
    headers = {"auth": "test"}

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{api_url}v1/generate/", json=data, headers=headers) as response:
            job_id = await response.json()
        while counter < timeout :
            async with session.get(api_url + f"v1/image/{job_id}/") as r:
                if r.status == 200:
                    url = await r.json()
                    return url
                await asyncio.sleep(0.5)
                counter += 0.5








generating_embed = discord.Embed(
        title="Generating Image",
        description="Image Is Generating, It takes 30 ~ 50 seconds to generate",
        color=discord.Color.orange()
    )





class RetryButton(ui.View):
    def __init__(self, prompt, model, user, p1) -> None:
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.user = user
        self.p1 = p1
            
            
    @discord.ui.button(label='retry', emoji="♻️", style=discord.ButtonStyle.green, custom_id='retry')
    async def retry(self, interaction: discord.Interaction, button: ui.Button):
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.edit_message(content=None, embed=generating_embed)
        
        image = await generate_image(self.prompt, self.model)
        
        
        if image:
            print(f"Prompt: {self.prompt}\nImage URL: {image}") 
            image_embed = discord.Embed(title="Generated Image", color=discord.Color.blue())
            image_embed.set_image(url=image)
            image_embed.add_field(name="Prompt", value=self.prompt, inline=False)
            image_embed.add_field(name="Model", value=self.model, inline=False)
            button.disabled = False
            await interaction.message.edit(view=self)
            await interaction.edit_original_response(content=None, embed=image_embed)

            
            
        else:
            await interaction.response.edit_message(content="Failed to upload image.", embed=None)
            
    async def interaction_check(self, interaction):
        if interaction.user.id != self.p1:
            await interaction.response.send_message(f"You do not own this command {interaction.user.mention}", ephemeral= True)
        return interaction.user.id == self.p1




async def check_words(prompt: str) -> bool:
    banned_patterns = [
        r"\bloli\b",
        r"\bbaby\b",
        r"\bshota\b",
        r"\bunderage\b",
        r"\bkid\b",
        r"\bchild\b",
        r"\blittle girl\b",
        r"\byoung girl\b",
        r"\bpetite\b",
        r"\blittle boy\b",
        r"\byoung boy\b",
        r"\bteen\b",
        r"\btween\b",
        r"\bminor\b",
        r"\badolescent\b",
        r"\bpreteen\b",
        r"\bsmall girl\b",
        r"\bsmall boy\b",
        # Match age patterns only if the age is below 18
        r"\b(1[0-7]|[1-9])\s?yo\b",                # e.g., 2yo, 15yo (but not 18yo or older)
        r"\b(1[0-7]|[1-9])\s?years?\s?old\b",       # e.g., 3 years old, 10 yrs old (but not 18 or older)
        r"\b(1[0-7]|[1-9])\s?-year-old\b",          # e.g., 4-year-old, 7-year-old (but not 18 or older)
    ]

    prompt_lower = prompt.lower()
    for pattern in banned_patterns:
        if re.search(pattern, prompt_lower):
            return True
    return False









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
        await asyncio.sleep(1800)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.type == discord.ChannelType.private:
        title = 'The Bot Can Only Be Used In Servers'
    else:
        title='Bot Is Now Based On / Commands Only'
        
    response_embed = discord.Embed(title=title,
            description=f"[Invite](https://discord.com/oauth2/authorize?client_id=1180105597874610206&permissions=277025515584&scope=bot) the bot for your server!\n[Support](https://discord.com/invite/bVUa2En9) our community server!",
            color=discord.Color.blue())
    
    if message.content == client.user.mention:
        await message.channel.send(embed=response_embed)

    await client.process_commands(message)

    
@tree.command(name = "stats", description = "Get bot statistics")
async def stats(interaction: discord.Interaction):
    total_servers = len(client.guilds)
    total_members = sum(guild.member_count for guild in client.guilds)
    uptime = datetime.datetime.now(datetime.timezone.utc) - start_time
    total_seconds, microseconds = divmod(uptime.microseconds + (uptime.seconds + uptime.days * 86400) * 10 ** 6, 10 ** 6)
    days = int(total_seconds // 86400)
    uptime_string = f"{days} days, {int((total_seconds % 86400) // 3600)} hours, {int((total_seconds % 3600) // 60)} minutes, {int(total_seconds % 60)} seconds, and {int(microseconds)} microseconds"
    embed = discord.Embed(
        title = "Bot Statistics",
        description = f"Here are the current statistics of the bot:\n\nTotal Servers: {total_servers}\nTotal Members: {total_members}\nUptime: {uptime_string}",
        color = discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)
    
     
@client.command(name="machine", description="Get bot's machine statistics")
async def machine(ctx):
    try:
        ram = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        disk = psutil.disk_usage('/')

        performance_rate = int((ram.percent + cpu + disk.percent) / 3)

        embed = discord.Embed(title="Machine Stats", color=discord.Color.blue())
        embed.add_field(name="Free RAM", value=f"{ram.available / (1024 ** 3):.2f} GB / {ram.total / (1024 ** 3):.2f} GB", inline=True)
        embed.add_field(name="Free CPU", value=f"{100 - cpu:.2f}%", inline=True)
        embed.add_field(name="Free Disk Space", value=f"{disk.free / (1024 ** 3):.2f} GB / {disk.total / (1024 ** 3):.2f} GB", inline=True)
        embed.add_field(name="Performance Rate", value=f"{performance_rate}% out of 100%", inline=False)

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.event
async def on_guild_join(guild):
    # Details about the server
    owner = guild.owner
    server_name = guild.name
    if owner:  # Ensure there is an owner object
        owner_name = f"{owner.name}#{owner.discriminator}"  # The owner's username and discriminator
        owner_id = owner.id  # The owner's ID

        # Construct the message
        message_content = f"{owner_name} (ID: {owner_id}) added the bot to their server {server_name}."

        # Fetch your user object by your Discord user ID
        user = await client.fetch_user(761886210120744990)  # Your Discord ID

        # Send the message
        if user:
            await user.send(message_content)
        else:
            print("Failed to fetch user for DM.")
    else:
        print("Failed to retrieve owner information.")




@client.command()
async def imagine(ctx, *, prompt: str):
    message = await ctx.send(embed=generating_embed)
    if await check_words(prompt):
        return await message.edit(content="your prompt contain banned word", embed=None)
    image = await generate_image(prompt, model="Realistic_Vision_v5.0")


    if image:
        view=RetryButton(prompt, model, ctx.user.name, ctx.user.id)
        
        image_embed = discord.Embed(title="Generated Image", color=discord.Color.blue())
        image_embed.set_image(url=image)
        image_embed.add_field(name="Prompt", value=prompt, inline=False)
        image_embed.add_field(name="Model", value="Realistic_Vision_v5.0", inline=False)

        await message.edit(content=None, embed=image_embed, view = view)
        print(f"Image URL: {image}")  # Log the image URL to the console
    else:
        await message.edit(content="Failed to upload image.", embed=None)

    

#how to use
@tree.command(description="generate images by ai")
@app_commands.describe(prompt="description of the image", private="make the image visble for you or everyone", image_type="type of the image like anime, 3d, etc...")
@app_commands.choices(
    private = [
    app_commands.Choice(name="True", value="True"),
    app_commands.Choice(name="False", value="False"),
    ],
    image_type = [
        app_commands.Choice(name="default・realistic", value="Realistic_Vision_v5.0"),
        app_commands.Choice(name="3D", value="lyriel_v1.6"),
        app_commands.Choice(name="anime", value="anything_V5"),

        ]
    
)
async def imagine(ctx : discord.Interaction, prompt: str, image_type: app_commands.Choice[str] = None, private: app_commands.Choice[str] = None):
    private_value = True if private is not None and private.value == "True" else False 
    model = image_type.value if image_type is not None else "Realistic_Vision_v5.0"
    
    await ctx.response.send_message(embed=generating_embed, ephemeral=bool(private_value))
    if await check_words(prompt):
        return await ctx.edit_original_response(content="your prompt contain banned word", embed=None)


    image = await generate_image(prompt, model)
    
    
    if image:
        view=RetryButton(prompt, model, ctx.user.name, ctx.user.id)
        print(f"Prompt: {prompt}\nImage URL: {image}") 
        image_embed = discord.Embed(title="Generated Image", color=discord.Color.blue())
        image_embed.set_image(url=image)
        image_embed.add_field(name="Prompt", value=prompt, inline=False)
        image_embed.add_field(name="Model", value=model, inline=False)
        await ctx.edit_original_response(content=None, embed=image_embed, view=view)
        
        
    else:
        
        await ctx.edit_original_response(content="Failed to upload image.", embed=None)

    
client.run("")#use your bot token
