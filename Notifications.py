# ------------------- IMPORT STATEMENTS -------------------#
import json
from discord import Webhook, SyncWebhook, File, Colour, Embed
from tokens import WEBHOOK

# ------------------- INITIALIZATION VARIABLES -------------------#

webhookLink = WEBHOOK
webhook = SyncWebhook.from_url(webhookLink)

botUsername = "cologne-bot"

# All ID's necessary to ping specific users / roles
userPing = "<@578669410378711066> <@714646955380441148> <@546848918160539651>"  # User ID Me, Rashad, Aatmayan
pIncreasePing = "<@&1512544144910975056>"  # Role ID for price increase role
pDecreasePing = "<@&1512544292323983420>"  # Price decrease role
qIncreasePing = "<@&1512544384132845638>"  # Quantity increase role
qDecreasePing = "<@&1512544326981517425>"  # Quantity decrease role

# ------------------- FUNCTIONS / METHODS -------------------#


# Creates an embed to detail when a product has increased in price
def priceIncrease(title, newPrice, oldPrice, imgLink, productLink):
    # Create the embed
    embed = Embed(
        title=title,
        description="A price increase has been detected on this fragrance.",
        color=Colour.dark_red(),
        url=productLink,
    )

    embed.set_author(name="💵 📈 Price Increase")
    embed.add_field(name="Was:", value=(f"~~**${oldPrice}**~~"), inline=True)
    embed.add_field(name="Now:", value=(f"**${newPrice}**"), inline=True)
    embed.add_field(
        name="Increase:", value=f"**+${abs(newPrice-oldPrice)}**", inline=True
    )
    embed.set_thumbnail(url=imgLink)
    embed.set_footer(text="Cologne Tracker • Shayaan Shahid")

    # Send the embed to the discord channel
    webhook.send(
        content=pIncreasePing + getRoleID(title),
        username=botUsername,
        embed=embed,
    )


# Creates an embed to detail when a product has decreased in price
def priceDecrease(title, newPrice, oldPrice, imgLink, productLink):
    # Create the embed
    embed = Embed(
        title=title,
        description="A price decrease has been detected on this fragrance.",
        color=Colour.dark_green(),
        url=productLink,
    )

    embed.set_author(name="💵 📉 Price Decrease")
    embed.add_field(name="Was:", value=(f"~~**${oldPrice}**~~"), inline=True)
    embed.add_field(name="Now:", value=(f"**${newPrice}**"), inline=True)
    embed.add_field(
        name="Decrease:", value=f"**-${abs(newPrice-oldPrice)}**", inline=True
    )
    embed.set_thumbnail(url=imgLink)
    embed.set_footer(text="Cologne Tracker • Shayaan Shahid")

    # Send the embed to the discord channel
    webhook.send(
        content=pDecreasePing + getRoleID(title),
        username=botUsername,
        embed=embed,
    )


# Creates an embed to detail when a product has been restocked (increase quantity)
def quantityIncrease(title, newQuantity, oldQuantity, imgLink, productLink):
    # Create the embed
    embed = Embed(
        title=title,
        description=f"{abs(newQuantity-oldQuantity)} units of this product have been restocked!",
        color=Colour.dark_green(),
        url=productLink,
    )

    embed.set_author(name="📦 Restock")
    embed.add_field(
        name="# Unit(s) Before:", value=(f"~~**{oldQuantity}**~~"), inline=True
    )
    embed.add_field(name="# Unit(s) Now:", value=(f"**{newQuantity}**"), inline=True)
    embed.set_thumbnail(url=imgLink)
    embed.set_footer(text="Cologne Tracker • Shayaan Shahid")

    # Send the embed to the discord channel
    webhook.send(
        content=qIncreasePing + getRoleID(title),
        username=botUsername,
        embed=embed,
    )


# Creates an embed to detail when a product has been sold (decrease quantity)
def quantityDecrease(title, newQuantity, oldQuantity, imgLink, productLink):
    # Create the embed
    embed = Embed(
        title=title,
        description=f"{abs(newQuantity-oldQuantity)} unit(s) of this product were purchased.",
        color=Colour.dark_red(),
        url=productLink,
    )

    embed.set_author(name="🛒 Stock Decrease")
    embed.add_field(
        name="# Unit(s) Before:", value=(f"~~**{oldQuantity}**~~"), inline=True
    )
    embed.add_field(name="# Unit(s) Now:", value=(f"**{newQuantity}**"), inline=True)
    embed.set_thumbnail(url=imgLink)
    embed.set_footer(text="Cologne Tracker • Shayaan Shahid")

    # Send the embed to the discord channel
    webhook.send(
        content=qDecreasePing + getRoleID(title),
        username=botUsername,
        embed=embed,
    )


# Takes the role ID for the cooresponding role, allowing to ping all users tracking a particular fragrance
def getRoleID(roleTitle):
    try:
        with open("roles&ID.json", "r") as file:
            data = json.load(file)
            roleID = data[str(roleTitle)]

    except:
        roleID = None

    if roleID is not None:
        roleID = f"<@&{roleID}>"
        return roleID
    else:
        return ""


# ------------------- QUICK TESTS -------------------#

# priceIncrease(
#     "Christian Dior Sauvage EDT M 60ml Boxed",
#     100,
#     50,
#     "https://cdn.shopify.com/s/files/1/0274/8363/files/sauvageedpedition-man_df9df031-3421-438f-b11e-d1105a979811.jpg?v=1780008203",
#     "https://fragrancebuy.ca/products/sauvageedpedition-man",
# )

# priceDecrease(
#     "Christian Dior Sauvage EDT M 60ml Boxed",
#     50,
#     150,
#     "https://cdn.shopify.com/s/files/1/0274/8363/files/sauvageedpedition-man_df9df031-3421-438f-b11e-d1105a979811.jpg?v=1780008203",
#     "https://fragrancebuy.ca/products/sauvageedpedition-man",
# )
