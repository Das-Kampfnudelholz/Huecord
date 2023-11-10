import interactions
import os
import json
import requests
import asyncio
import aiohttp
import sys
import random
import time

def hex_to_hue(hex_code):
    # Convert HEX code to RGB values
    r, g, b = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
    
    # Convert RGB values to XY values
    red = (r + 0.055) / (1.0 + 0.055)
    green = (g + 0.055) / (1.0 + 0.055)
    blue = (b + 0.055) / (1.0 + 0.055)
    
    red = pow(red, 2.4) if red > 0.04045 else (red / 12.92)
    green = pow(green, 2.4) if green > 0.04045 else (green / 12.92)
    blue = pow(blue, 2.4) if blue > 0.04045 else (blue / 12.92)
    
    X = red * 0.649926 + green * 0.103455 + blue * 0.197109
    Y = red * 0.234327 + green * 0.743075 + blue * 0.022598
    Z = red * 0.0000000 + green * 0.053077 + blue * 1.035763
    
    x = X / (X + Y + Z)
    y = Y / (X + Y + Z)
    
    # Convert XY values to Hue values
    hue_x = int(x * 65535)
    hue_y = int(y * 65535)
    
    # Return Hue color code
    return [hue_x, hue_y]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#Creates Config File if missing#
if not 'Config.json' in os.listdir():
    open('Config.json', 'w').write('{"guild_id":"", "bot_token":"", "hue_username":"", "hue_access":""}')
    print(bcolors.WARNING + "Warning: Config has been created. Restart Tool after filling info" + bcolors.ENDC)
#################################

#Function to check the config#
def check_config(config):
    for key, value in config.items():
        if value == "":
            raise ValueError(f"The configuration for '{key}' cannot be empty. Please fill out the Config.json file.")
##########################

#Check the config#
try:
    # Geting Values from Config File
    with open("Config.json", "r") as config_file:
        config = json.load(config_file)
        # Check if any configuration values are empty
        check_config(config)
        # ... rest of your code to set up the bot ...
except ValueError as e:
    print(e)
    sys.exit(1)
##################

#Getting Values from Config File#
with open("Config.json", "r") as config_file:
    config = json.load(config_file)
    discord_token = config['bot_token']
    guild_id = config['guild_id']
    hue_username = config['hue_username']
    hue_access = config['hue_access']
    hue_url = f"https://api.meethue.com/bridge/{hue_username}/groups/0/action"
    hue_headers = {"Content-Type": "application/json", "Authorization": "Bearer " + hue_access}
################################

#Initialize the bot#
bot = interactions.Client(token=discord_token)
################################

##### Start Print #####
@bot.event
async def on_ready():
    print(bcolors.OKGREEN + f"Info: Bot running as {bot.me.name}" + bcolors.ENDC)
#######################

##### Help Command #####
@bot.command(
    name="help",
    description="Shows all commands"
)
async def help(ctx: interactions.CommandContext):
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='Commands', value='`/on` \n`/off` \n`/brightness` \n`/white` \n`/red` \n`/color`\n`/nosleep`\n`/disco`\n`/rainbow`', inline=True)
    embed.add_field(name='Description',
                    value='Turns on the Lights \nTurns the Lights off \n Adjust the Brightness of all Lights \nTurns the Lights white \nTurns the Lights red \nSets the Lights to a custom Color using Hex Color inputs \nSets an time where the light turn on (24h time format)(SOON)\nActivate Disco Mode for 10 Seconds\nToggle of Rainbow Disco Lights ',
                    inline=True)

    await ctx.send(embeds=embed)
    print(bcolors.OKCYAN + "Log: /help Executed" + bcolors.ENDC)
########################

#### Status Command ####
@bot.command(
    name="status",
    description="Get the status of the lights"
)
async def status(ctx: interactions.CommandContext):
    # Assuming 'hue_url' is the base URL for your Hue Bridge
    # and 'hue_headers' includes the necessary authorization headers
    status_url = f"{hue_url}/lights"  # Update this if you have a specific light ID in mind

    async with aiohttp.ClientSession() as session:
        async with session.get(status_url, headers=hue_headers) as response:
            if response.status == 200:
                # The response body will contain the status of the lights
                lights_status = await response.json()
                # Format the status in a user-friendly way
                status_message = format_lights_status(lights_status)
                await ctx.send(status_message)
            else:
                # Handle possible errors
                await ctx.send("Failed to retrieve the status of the lights.")

def format_lights_status(lights_status):
    # This function takes the JSON response and formats it into a string.
    # You'll need to customize this based on how you want to display the status.
    status_lines = []
    for light_id, info in lights_status.items():
        on_state = "On" if info['state']['on'] else "Off"
        brightness = info['state'].get('bri', 'Unknown')  # Brightness might not be available
        status_line = f"Light {light_id} is {on_state}, Brightness: {brightness}"
        status_lines.append(status_line)
    return "\n".join(status_lines)
########################

###### On Command ######
@bot.command(
    name="on",
    description="Turns on the lights"
)
async def on(ctx: interactions.CommandContext):
    data = {"on": True}
    response = requests.put(hue_url, headers=hue_headers, json=data)
    await ctx.send(f"Lights have been turned on. Status: {response.status_code}")
    print(bcolors.OKCYAN + "Log: /on Executed" + bcolors.ENDC)
########################

###### Off Command ######
@bot.command(
    name="off",
    description="Turns the lights off"
)
async def off(ctx: interactions.CommandContext):
    data = {"on": False}
    response = requests.put(hue_url, headers=hue_headers, json=data)
    await ctx.send(f"Lights have been turned off. Status: {response.status_code}")
    print(bcolors.OKCYAN + "Log: /off Executed" + bcolors.ENDC)
########################

###### Brightness Command ######
@bot.command(
    name="brightness",
    description="Adjust the brightness of the lights",
    options=[
        interactions.Option(
            name="level",
            description="Brightness level (0-254)",
            type=interactions.OptionType.INTEGER,
            required=True
        )
    ]
)
async def brightness(ctx: interactions.CommandContext, level: int):
    data = {"on": True, "bri": level}
    response = requests.put(hue_url, headers=hue_headers, json=data)
    await ctx.send(f"Brightness set to {level}. Status: {response.status_code}")
    print(bcolors.OKCYAN + f"Log: /brightness {level} Executed" + bcolors.ENDC)
########################

###### White Command ######
@bot.command(
    name="white",
    description="Sets the lights to white"
)
async def white(ctx: interactions.CommandContext):
    data = {"on": True, "bri": 254, "ct": 350}
    response = requests.put(hue_url, headers=hue_headers, json=data)
    await ctx.send(f"Lights have been set to white. Status: {response.status_code}")
    print(bcolors.OKCYAN + "Log: /white Executed" + bcolors.ENDC)
########################

###### Red Command ######
@bot.command(
    name="red",
    description="Sets the lights to red"
)
async def red(ctx: interactions.CommandContext):
    data = {"on": True, "bri": 254, "hue": 0, "sat": 254}
    response = requests.put(hue_url, headers=hue_headers, json=data)
    await ctx.send(f"Lights have been set to red. Status: {response.status_code}")
    print(bcolors.OKCYAN + "Log: /red Executed" + bcolors.ENDC)
########################



###### Color Command ######
@bot.command(
    name="color",
    description="Set the lights to a custom color using a HEX code",
    options=[
        interactions.Option(
            name="hex_code",
            description="Enter a HEX color code (without the #)",
            type=interactions.OptionType.STRING,
            required=True
        )
    ]
)
async def color(ctx: interactions.CommandContext, hex_code: str):
    # Convert HEX to Hue's CIE xy color space and clamp the values
    hue_color = hex_to_hue(hex_code)
    
    # Normalize the values for the Hue API (values between 0 and 1)
    xy_normalized = [hue_color[0] / 65535, hue_color[1] / 65535]

    # Logging the normalized xy values
    # print(f"Normalized XY values being sent: {xy_normalized}")

    # Data payload for the Hue API
    data = {"on": True, "xy": xy_normalized}

    # Sending the request asynchronously using aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.put(hue_url, headers=hue_headers, json=data) as response:
            # Get the response status and body for debugging
            status = response.status
            # response_body = await response.json()
            # print(f"Response from Hue: {response_body}")  # Debugging line

    # Responding to the Discord command
    await ctx.send(f"Lights have been set to {hex_code}. Status: {status}")
    print(bcolors.OKCYAN + f"Log: /color {hex_code} Executed" + bcolors.ENDC)
########################

###### Disco Command ######
disco_active = False

@bot.command(
    name="disco",
    description="Activate Disco Mode for the lights"
)
async def disco(ctx: interactions.CommandContext):
    global disco_active
    # Check if disco is already active
    if disco_active:
        await ctx.send("Disco is already running!")
        return

    # Acknowledge the command immediately
    await ctx.send("Disco mode activated for 30 seconds!")
    disco_active = True

    # Run the disco sequence in a background task
    asyncio.create_task(run_disco_sequence(ctx))

@bot.command(
    name="stop_disco",
    description="Stop Disco Mode for the lights"
)
async def stop_disco(ctx: interactions.CommandContext):
    global disco_active
    # Stop the disco mode if it's active
    if disco_active:
        disco_active = False
        await ctx.send("Disco mode will stop shortly.")
    else:
        await ctx.send("Disco mode is not currently running.")

async def run_disco_sequence(ctx: interactions.CommandContext):
    global disco_active
    async with aiohttp.ClientSession() as session:
        # Ensure lights are on for disco effect
        initial_data = {"on": True}
        await session.put(hue_url, headers=hue_headers, json=initial_data)
        
        start_time = time.time()
        duration = 30  # seconds
        requests_per_second = 10  # Hue Bridge rate limit
        min_delay = 1 / requests_per_second

        while time.time() - start_time < duration and disco_active:
            delay = random.uniform(min_delay, 0.2)
            disco_data = {
                "on": True,
                "bri": 254,
                "hue": random.randint(0, 65535),
                "sat": 254,
                "transitiontime": 2
            }
            await session.put(hue_url, headers=hue_headers, json=disco_data)
            await asyncio.sleep(delay)

        # Turn off disco mode
        disco_active = False
        # Edit the original response to indicate completion
        await ctx.edit("No more disco :(")
        
    print(bcolors.OKCYAN + "Log: /disco Executed" + bcolors.ENDC)
########################

###### Rainbow Command ######
@bot.command(
    name="rainbow",
    description="Toggle rainbow effect for the lights",
    options=[
        interactions.Option(
            name="state",
            description="Choose 'on' to activate or 'off' to deactivate",
            type=interactions.OptionType.STRING,
            required=True,
            choices=[
                interactions.Choice(name="on", value="on"),
                interactions.Choice(name="off", value="off")
            ]
        )
    ]
)
async def rainbow(ctx: interactions.CommandContext, state: str):
    data = {"on": True, "effect": 'colorloop'} if state == "on" else {"effect": 'none'}
    response = requests.put(hue_url, headers=hue_headers, json=data)
    action = "activated" if state == "on" else "deactivated"
    await ctx.send(f"Rainbow effect has been {action}. Status: {response.status_code}")
    print(bcolors.OKCYAN + f"Log: /rainbow {state} Executed" + bcolors.ENDC)
########################

## running the Discord Bot ##
bot.start()
#############################