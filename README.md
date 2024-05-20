# AI Image Generator Discord Bot

This Discord bot utilizes an AI image generation API to create images based on user prompts. It supports both traditional command-based interaction as well as slash commands.

## Features

- **Image Generation**: Users can generate images by providing prompts to the bot. The bot then utilizes an AI model to generate an image based on the prompt.
- **Slash Commands**: The bot supports slash commands for streamlined interaction and ease of use.
- **Customization**: Users can customize the image format, type, and visibility of generated images.

## Commands

### Traditional Commands

- **>imagine [prompt]**: Generate an image based on the provided prompt.
  - Example: `>imagine A beautiful sunset over the mountains`

### Slash Commands

- **/imagine**: Generate an image using a slash command.
  - Options:
    - **prompt**: Description of the image.
    - **private**: Make the image visible for you or everyone.
    - **image_format**: The format of the image (e.g., default, portrait, landscape).
    - **image_type**: Type of the image (e.g., realistic, 3D, anime).

## Setup

1. Clone this repository.
2. Install dependencies by running `pip install -r requirements.txt`.
3. Create a new Discord bot and obtain its token:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a new application and navigate to the "Bot" tab.
   - Click "Add Bot" to create a bot user for your application.
   - Copy the token provided under the bot's username and avatar.
4. Replace the `client.run("")` line in `bot.py` with your Discord bot token.
5. Run the bot using `python bot.py`.


## Dependencies

- `discord.py`: Discord API wrapper for Python.
- `aiohttp`: Asynchronous HTTP client/server framework.
- `asyncio`: Asynchronous I/O support.
- `datetime`: Date and time manipulation.


## Thanks

- thanks to [OpenImagery](https://discord.gg/9z2wBmdQdS) for  providing a free AI api
