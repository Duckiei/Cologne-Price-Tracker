# ------------------- FUNCTIONS / METHODS -------------------#
import discord
from discord.ext import commands
import Database
import Webscraper
import json

# ------------------- INITIALIZATION VARIABLES -------------------#
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Name of each general notification role
rolePI = "notify-price-increase"
rolePD = "notify-price-decrease"
roleQI = "notify-units-sold"
roleQD = "notify-units-restocked"
alrole = "notify-price-increasenotify-price-decreasenotify-units-soldnotify-units-restocked@everyone"


# ------------------- FUNCTIONS / METHODS -------------------#


# Small startup message
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


# Provides a .txt file in discord channel for user to see all tracked products
@bot.command()
async def tables(ctx):
    tables = Database.getTables()
    tables.sort()

    with open("tables.txt", "w") as names:
        for table in tables:
            names.write(table + "\n")

    await ctx.channel.send(
        content="Current tables in the database:",
        file=discord.File("tables.txt"),
    )


# Make user be notified when ANY product increases in price
@bot.command()
async def notifypriceincreases(ctx):
    await ctx.message.delete()

    roleName = rolePI
    message = "products increase in price"

    role = discord.utils.get(ctx.guild.roles, name=roleName)

    if role:
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.channel.send(
                f"{ctx.author.mention} will not be notified when {message}."
            )
        else:
            await ctx.author.add_roles(role)
            await ctx.channel.send(
                f"{ctx.author.mention} will now be notified when {message}."
            )

    else:
        await ctx.channel.send(f"Role deprecated")


# Make user be notified when ANY product decreases in price
@bot.command()
async def notifypricedecreases(ctx):
    await ctx.message.delete()

    roleName = rolePD
    message = "products decrease in price"

    role = discord.utils.get(ctx.guild.roles, name=roleName)

    if role:
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.channel.send(
                f"{ctx.author.mention} will not be notified when {message}."
            )
        else:
            await ctx.author.add_roles(role)
            await ctx.channel.send(
                f"{ctx.author.mention} will now be notified when {message}."
            )

    else:
        await ctx.channel.send(f"Role deprecated")


# Make user be notified when ANY product increases in quantity
@bot.command()
async def notifyquantityincreases(ctx):
    await ctx.message.delete()

    roleName = roleQI
    message = "product units are restocked"

    role = discord.utils.get(ctx.guild.roles, name=roleName)

    if role:
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.channel.send(
                f"{ctx.author.mention} will not be notified when {message}."
            )
        else:
            await ctx.author.add_roles(role)
            await ctx.channel.send(
                f"{ctx.author.mention} will now be notified when {message}."
            )

    else:
        await ctx.channel.send(f"Role deprecated")


# Make user be notified when ANY product decreases in quantity
@bot.command()
async def notifyquantitydecreases(ctx):
    await ctx.message.delete()

    roleName = roleQD
    message = "product units are sold"

    role = discord.utils.get(ctx.guild.roles, name=roleName)

    if role:
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.channel.send(
                f"{ctx.author.mention} will not be notified when {message}."
            )
        else:
            await ctx.author.add_roles(role)
            await ctx.channel.send(
                f"{ctx.author.mention} will now be notified when {message}."
            )

    else:
        await ctx.channel.send(f"Role deprecated")


# Start tracking product w the provided link (multiple links can be entered with one call, using spaces to seperate links)
@bot.command()
async def add(ctx, *, urls):
    if ctx.author.id == 578669410378711066:
        if " " in str(urls):
            toTrack = str(urls).split(" ")

            with open("fragranceBuy-Sites.txt", "a") as file:
                for cologne in toTrack:
                    file.write("\n" + cologne)
                    Webscraper.scrapeOne(cologne)

            await ctx.channel.send("Scraped multiple Links")

        else:
            with open("fragranceBuy-Sites.txt", "a") as file:
                file.write("\n" + urls)
                Webscraper.scrapeOne(urls)

            await ctx.channel.send("Scraped Single Link")

    else:
        ctx.channel.send("You do not have proper permissions to add colognes")


# Small summary card of all live information for specified cologne (top right part of DASH interface basically)
@bot.command()
async def status(ctx, *, productTitle):
    # Retrieve the url of desired product
    try:
        url = Database.getURL(productTitle)
    except Exception:
        await ctx.channel.send(
            f'The fragrance "{productTitle}" does not exist, or is not currently being tracked.'
        )
        return

    current_price, current_quantity, regular_price, description, img = (
        Webscraper.scrapeLiveData(url=url)
    )

    # Create embed
    embed = discord.Embed(
        title=productTitle,
        description=f'"{description}"',
        color=discord.Colour.dark_purple(),
        url=url,
    )

    embed.set_author(name="❗Live Status")
    embed.add_field(
        name="# Unit(s) in Stock", value=(f"**{current_quantity}**"), inline=True
    )
    embed.add_field(name="Current Price:", value=(f"**${current_price}**"), inline=True)
    embed.set_thumbnail(url=img)
    embed.set_footer(text="Cologne Tracker • Shayaan Shahid")

    # Send embed
    await ctx.channel.send(embed=embed)


# Make user be notified whenever a SPECIFIC product is changed (all 4 changes)
@bot.command()
async def track(ctx, *, roleName):
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    tables = Database.getTables()

    # If that role exists, then assign it to the person, if it doesn't, create it and assign it to the person
    if not role and roleName in tables:
        # Create the role
        await ctx.guild.create_role(name=roleName)
        role = discord.utils.get(ctx.guild.roles, name=roleName)

        # Write to json file
        with open("roles&ID.json", "r") as file:
            data = json.load(file)

        with open("roles&ID.json", "w") as file:
            data[str(roleName)] = str(role.id)
            json.dump(data, file, indent=4)

    await ctx.author.add_roles(role)
    await ctx.channel.send(f"Added role - Started tracking: {roleName}")


# Stop tracking SPECIFIC product changes (all 4 changes)
@bot.command()
async def untrack(ctx, *, roleName):
    # Remove the role from the person, and if the amount of people that have that role == 0, delete that role
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    tables = Database.getTables()

    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.channel.send(f"Removed role - Stopped tracking: {roleName}")

    if len(role.members) <= 0:
        await role.delete()
        await ctx.channel.send(f"Deleted role - Nobody is tracking: {roleName}")
        # Write to json file
        with open("roles&ID.json", "r") as file:
            data = json.load(file)

        with open("roles&ID.json", "w") as file:
            data.pop(roleName)
            json.dump(data, file, indent=4)


# Send user a list of all fragrances that they are tracking
@bot.command()
async def tracking(ctx):
    await ctx.channel.send("Here is what you are currently tracking: ")
    for role in ctx.author.roles:
        if role.name not in alrole:
            await ctx.channel.send(f"→ {role.name}")


bot.run("MTUxMTQ2NDk4NzU0Mzk5NDU0MA.G2I2Lf.tcCX1k5WoCcoF5IonylV9Byk3AwJht8j1Q-J24")
