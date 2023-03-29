import interactions 
import os
import json
import discord
import requests
from discord_slash import SlashCommand, SlashContext

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
async def abc(sid, id):
    slash = SlashCommand(bot, sync_commands=True)
#Geting Values from Config File#
txtconfig = json.loads(open("Config.json", "r").read())
discord_token =  txtconfig['bot_token']
guild_id =  txtconfig['guild_id']
hue_username =  txtconfig['hue_username']
hue_access =  txtconfig['hue_access']
url = "https://api.meethue.com/bridge/" + hue_username + "/groups/0/action"
headers = {"Content-Type": "application/json", "Authorization":hue_access}
bot = interactions.Client(token=discord_token, presence="Controling Philips Hue Lights")
################################

##### NEED TO FIX USERNAME #####
@bot.event
async def on_ready():
    print(bcolors.OKGREEN + "Info: Bot running as  " + bcolors.ENDC)
################################

##### Help Command #####
@bot.command()
async def help(ctx):
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='Commands', value='`/on` \n`/off` \n`/brightness` \n`/white` \n`/red` \n`/custom`\n`/nosleep`\n`/disco`\n`/rainbow`', inline=True)
    embed.add_field(name='Description',
                    value='Turns on the Lights \nTurns the Lights off \n Adjust the Brightness of all Lights \nTurns the Lights white \nTurns the Lights red \nSets the Lights to a custom Color using Hex Color inputs \nSets an time where the light turn on (24h time format)(SOON)\nActivate Disco Mode for 10 Seconds\nToggle of Rainbow Disco Lights ',
                    inline=True)

    await ctx.send(embeds=embed)
    print(bcolors.OKCYAN + "Log: /help Executed" + bcolors.ENDC)
########################

###### On Command ######
@bot.command()
async def on(ctx):
    data = {"on": True}
    response = requests.put(url, headers=headers, json=data)
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='State', value='Lights have been tunred on', inline=True)
    await ctx.send(embeds=embed)

    print(bcolors.OKCYAN + "Log: /on Executed" + bcolors.ENDC)
########################

###### Off Command ######
@bot.command()
async def off(ctx):
    data = {"on": False}
    response = requests.put(url, headers=headers, json=data)
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='State', value='Lights have been tunred off', inline=True)
    await ctx.send(embeds=embed)
    print(bcolors.OKCYAN + "Log: /off Executed" + bcolors.ENDC)
########################

###### Brightness Command ######
@bot.command(
        name="brightness",
        description="Set the Brightness",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="brightness",
                    description="Set the Brightness between 0-254",
                    type=interactions.OptionType.STRING,
                    required=True,
        ),
    ],
)
async def brightness(ctx,
    *content,
    brightness: str,):
    data = {"on": False, "bri": brightness}
    response = requests.put(url, headers=headers, json=data)
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='State', value='Lights have been set to ' + brightness, inline=True)
    await ctx.send(embeds=embed)
    print(bcolors.OKCYAN + "Log: /brightness " + brightness + " Executed" + bcolors.ENDC)
########################

###### White Command ######
@bot.command()
async def white(ctx):
    data = {"on": True, "bri": 254, "ct": 350}
    response = requests.put(url, headers=headers, json=data)
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='State', value='Lights have been tunred White', inline=True)
    await ctx.send(embeds=embed)
    print(bcolors.OKCYAN + "Log: /white Executed" + bcolors.ENDC)
########################

###### Red Command ######
@bot.command()
async def red(ctx):
    data = {"on": True, "bri": 254, "hue": 0, "sat": 254}
    response = requests.put(url, headers=headers, json=data)
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='State', value='Lights have been tunred Red', inline=True)
    await ctx.send(embeds=embed)
    print(bcolors.OKCYAN + "Log: /red Executed" + bcolors.ENDC)
########################


###### Color Command ######
@bot.command(
        name="color",
        description="Set the Color via HEX",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="color",
                    description="Set the Color via HEX",
                    type=interactions.OptionType.STRING,
                    required=True,
        ),
    ],
)
async def color(ctx,
    *content,
    color: str,):
    huecolor = hex_to_hue(color)
    data = {"on": True, "bri": 254, "hue":huecolor[0], "hue":huecolor[1] }
    response = requests.put(url, headers=headers, json=data)
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='State', value='Lights have been set to ' + color, inline=True)
    await ctx.send(embeds=embed)
    print(bcolors.OKCYAN + "Log: /color " + color + " Executed" + bcolors.ENDC)
########################

###### Disco Command ######
@bot.command()
async def disco(ctx):
    embed = interactions.Embed(title='', description=f'', color=0x00E043)
    embed.add_field(name='State', value='Lights have been tunred into Disco mode for 10 Secconds ', inline=True)
    await ctx.send(embeds=embed)
    data = {"on": False, "transitiontime":1}
    response = requests.put(url, headers=headers, json=data)
    data = {"on":True, "bri": 254, "hue": 0, "sat": 254, "transitiontime":3}
    response = requests.put(url, headers=headers, json=data)
    data = {"on":True, "bri": 254, "hue": 15350, "sat": 254, "transitiontime":3}
    response = requests.put(url, headers=headers, json=data)
    data = {"on":True, "bri": 254, "hue": 0, "sat": 254, "transitiontime":3}
    response = requests.put(url, headers=headers, json=data)
    data = {"on":True, "bri": 254, "hue": 15350, "sat": 254, "transitiontime":3}
    response = requests.put(url, headers=headers, json=data)
    data = {"on":True, "bri": 254, "hue": 0, "sat": 254, "transitiontime":3}
    response = requests.put(url, headers=headers, json=data)
    data = {"on":True, "bri": 254, "hue": 15350, "sat": 254, "transitiontime":4}
    response = requests.put(url, headers=headers, json=data)

    print(bcolors.OKCYAN + "Log: /disco Executed" + bcolors.ENDC)
########################

###### Rainbow Command ######
@bot.command(
        name="rainbow",
        description="Set the rainbow on/off",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="state",
                    description="Set the rainbow on/off",
                    type=interactions.OptionType.STRING,
                    required=True,
        ),
    ],
)
async def rainbow(ctx,
    *content,
    state: str,):
    if (state == "on"):
        data = {"on": True, "effect": 'colorloop' }
        response = requests.put(url, headers=headers, json=data)
        embed = interactions.Embed(title='', description=f'', color=0x00E043)
        embed.add_field(name='State', value='Lights have been set to rainbow' , inline=True)
        await ctx.send(embeds=embed)
    elif (state == "off"):
        data = {"effect": 'none' }
        response = requests.put(url, headers=headers, json=data)
        embed = interactions.Embed(title='', description=f'', color=0x00E043)
        embed.add_field(name='State', value='Lights have been set to normal' , inline=True)
        await ctx.send(embeds=embed)
    print(bcolors.OKCYAN + "Log: /rainbow" + state + " Executed" + bcolors.ENDC)
########################

## running the Discord Bot ##
bot.start()
#############################