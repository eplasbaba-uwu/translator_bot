import discord
from discord.ext import commands

import googletrans
from googletrans import Translator

import json
import os

if (os.path.exists(os.getcwd() + "/config.json")):
    with open("./config.json") as f:
        configdata = json.load(f)

else:
    configtemplate = {"Token": ""}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configtemplate, f)
token = configdata["Token"]

client = commands.Bot(command_prefix='t!', case_insensitive=True)
client.remove_command("help")
t = Translator()


@client.event
async def on_ready():
    print("Ready")


@client.command()
async def ping(ctx):
    await ctx.send(str(round((client.latency * 1000))) + "ms")


@client.group(invoke_without_command=True)
async def help(ctx):
    Embed = discord.Embed(title="Help", description="Type 't!help <command>' for information on that command(the name "
                                                    "of the command has to be in lower case)",
                          color=ctx.author.color)
    Embed.add_field(name="Translation Commands", value="translate,languages,detect")
    Embed.add_field(name="Other", value="ping", inline=False)
    await ctx.send(embed=Embed)


@help.command()
async def translate(ctx):
    Embed = discord.Embed(title="Translate Help", description="Translates text from one language to another, "
                                                              "for list of languages type 't!languages', the language "
                                                              "you want to translate into can either be the short "
                                                              "form of the language name or the full language name.If "
                                                              "you want to translate words that contain spaces, "
                                                              "put the text in quotes.",
                          color=ctx.author.color)

    Embed.add_field(name="Usage", value="t!translate <text> [language wanted to be translated in] {Language you are "
                                        "translating from, if empty it will default to english}")
    Embed.add_field(name="Example", value='t!translate "among us" arabic --> Translates text into arabic from english',
                    inline=False)
    Embed.add_field(name="Example",
                    value='t!translate أهلا english arabic --> Translates text into english from arabic', inline=False)
    await ctx.send(embed=Embed)


@help.command()
async def languages(ctx):
    Embed = discord.Embed(title="Language Help", description="DM's the user with a list of all the languages and "
                                                             "their short forms", color=ctx.author.color)

    Embed.add_field(name="Usage", value="t!languages")
    await ctx.send(embed=Embed)


@help.command()
async def detect(ctx):
    Embed = discord.Embed(title="Detection Help", description="Detects the language the user has given, it also "
                                                              "provides the confidence of its guess.If "
                                                              "you want to translate more than one word you need to "
                                                              "put the text in quotes",
                          color=ctx.author.color)

    Embed.add_field(name="Usage", value='t!detect <text>')
    Embed.add_field(name="Example", value='t!detect "among us"')
    await ctx.send(embed=Embed)


@help.command()
async def ping(ctx):
    Embed = discord.Embed(title="Ping Help", description="Shows the ping(latency) of the user, a higher ping might "
                                                         "lead to a slower response from the bot",
                          color=ctx.author.color)

    Embed.add_field(name="Usage", value="t!ping")
    await ctx.send(embed=Embed)


@client.command()
async def translate(ctx, text, s: str, *args):
    if args:
        txt = t.translate(text, src=args[0], dest=s)
        Embed = discord.Embed(title="Translate", color=ctx.author.color)
        Embed.add_field(name="Original Text", value=text)
        Embed.add_field(name="Translation", value=txt.text)
        await ctx.send(embed=Embed)
    else:
        txt = t.translate(text, src='en', dest=s)
        Embed = discord.Embed(title="Translate", color=ctx.author.color)
        Embed.add_field(name="Original Text", value=text)
        Embed.add_field(name="Translation", value=txt.text)
        await ctx.send(embed=Embed)


@client.command()
async def languages(msg):
    langs = googletrans.LANGUAGES
    await msg.author.send('\n'.join("{}-> {}".format(k, v) for k, v in langs.items()))
    author = msg.author.name
    await msg.send("Sent DM to " + "**" + author + "**")


@client.command()
async def detect(ctx, text):
    txt = t.detect(text)
    conf = round(float(txt.confidence) * 100)

    Embed = discord.Embed(title="Detect", color=ctx.author.color)
    Embed.add_field(name="Original text", value=text)
    Embed.add_field(name="Language Detection", value=txt.lang, inline=False)
    Embed.add_field(name="Confidence", value=str(conf) + "%", inline=False)
    await ctx.send(embed=Embed)


client.run(token)
# python3 translator.py
# imagine copying code
# kpop is stupid
