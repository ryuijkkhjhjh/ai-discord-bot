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
3. Obtain an API key from [VisionCraft Bot](https://t.me/VisionCraft_bot) and replace `api_key` in the code with your key.
4. Replace the `client.run("")` line with your Discord bot token.
5. Run the bot using `python bot.py`.

## Dependencies

- `discord.py`: Discord API wrapper for Python.
- `aiohttp`: Asynchronous HTTP client/server framework.
- `asyncio`: Asynchronous I/O support.
- `datetime`: Date and time manipulation.
