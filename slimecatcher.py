import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime, timedelta
from collections import Counter
from priv_info import BOT_TOKEN, ADMIN_ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

slime_adjectives = ["Squishy", "Gooey", "Slimy", "Sticky", "Slippery", "Jiggly", "Bubbly", "Sloppy", "Mushy", "Viscous",
                    "Glittering", "Iridescent", "Glistening", "Translucent", "Radiant", "Luminous", "Shimmering", "Opalescent", "Pulsating", "Sparkling",
                    "Freaky"]

slime_colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink", "Black", "White", "Brown",
                "Cyan", "Magenta", "Lime", "Teal", "Indigo", "Violet", "Maroon", "Olive", "Navy", "Turquoise"]

rarities = {
    "common": {"weight": 0.30, "color": 0x808080, "value": 50},  
    "uncommon": {"weight": 0.28, "color": 0x00FF00, "value": 100},  
    "rare": {"weight": 0.25, "color": 0x0000FF, "value": 200}, 
    "epic": {"weight": 0.15, "color": 0x800080, "value": 500},  
    "legendary": {"weight": 0.02, "color": 0xFFD700, "value": 2000}, 
    "ultimate legendary rainbow": {"weight": 0.001, "color": 0x000000, "value": 10000}  
}

cosmetic_items = [
    {"name": "Legendary Sword", "rarity": "Legendary", "price": 100000},
    {"name": "Epic Armor", "rarity": "Epic", "price": 50000},
    {"name": "Rare Helmet", "rarity": "Rare", "price": 25000},
    {"name": "Uncommon Shield", "rarity": "Uncommon", "price": 10000},
    {"name": "Common Boots", "rarity": "Common", "price": 5000},
    {"name": "Epic Bow", "rarity": "Epic", "price": 40000},
    {"name": "Rare Staff", "rarity": "Rare", "price": 20000},
    {"name": "Uncommon Wand", "rarity": "Uncommon", "price": 8000},
    {"name": "Common Potion", "rarity": "Common", "price": 6000},
    {"name": "Legendary Amulet", "rarity": "Legendary", "price": 90000}
]

catch_limits = {} 
user_slimes = {} 
user_balances = {} 
user_items = {}
duel_requests = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def catch(ctx):
    user_id = ctx.author.id
    now = datetime.now()
    
    if user_id not in catch_limits:
        catch_limits[user_id] = {"catches": 0, "reset_time": now + timedelta(hours=1)}
    
    if now >= catch_limits[user_id]["reset_time"]:
        catch_limits[user_id] = {"catches": 0, "reset_time": now + timedelta(hours=1)}
    
    if catch_limits[user_id]["catches"] >= 10:
        await ctx.send("You have reached your hourly catch limit.")
        return
    
    embed = discord.Embed(title="Catching...", description=f"{ctx.author.mention} has {10 - catch_limits[user_id]['catches']} more catches this hour.")
    await ctx.send(embed=embed)
    
    await asyncio.sleep(1) 
    
    catch_limits[user_id]["catches"] += 1
    
    caught = random.random() < 0.7
    if caught:
        rarity = random.choices(list(rarities.keys()), weights=[rarity["weight"] for rarity in rarities.values()])[0]
        if rarity == "ultimate legendary rainbow":
            slime_name = "ULTIMATE LEGENDARY RAINBOW SLIME!"
        else:
            adjective = random.choice(slime_adjectives)
            color = random.choice(slime_colors)
            slime_name = f"{rarity.capitalize()} {adjective} {color} Slime"
        
        if user_id not in user_slimes:
            user_slimes[user_id] = []
        user_slimes[user_id].append({"name": slime_name, "rarity": rarity})
        
        rarity_percentage = rarities[rarity]["weight"] * 100
        embed = discord.Embed(title="Slime Caught!", description=slime_name, color=rarities[rarity]["color"])
        embed.add_field(name="Rarity", value=f"{rarity.capitalize()} ({rarity_percentage:.2f}%)")
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Sorry {ctx.author.mention}! No slimes caught")

@bot.command()
async def slimes(ctx):
    user_id = ctx.author.id
    
    if user_id not in user_slimes or not user_slimes[user_id]:
        await ctx.send("You haven't caught any slimes yet.")
        return
    
    slimes_sorted = sorted(user_slimes[user_id], key=lambda x: list(rarities.keys()).index(x["rarity"]), reverse=True)
    highest_rarity = slimes_sorted[0]["rarity"]
    embed_color = rarities[highest_rarity]["color"]
    
    pages = [slimes_sorted[i:i+10] for i in range(0, len(slimes_sorted), 10)]
    
    for page in pages:
        embed = discord.Embed(title=f"{ctx.author.name}'s Slimes", color=embed_color)
        for slime in page:
            embed.add_field(name=slime["name"], value=f"Rarity: {slime['rarity'].capitalize()}")
        await ctx.send(embed=embed)

@bot.command()
async def bal(ctx):
    user_id = ctx.author.id
    if user_id not in user_balances:
        user_balances[user_id] = 0
    embed = discord.Embed(title=f"{ctx.author.name}'s Current Balance:", description=f"{user_balances[user_id]} coins", color=0xFFFF00)
    await ctx.send(embed=embed)

@bot.command()
async def sellall(ctx, rarity: str = None):
    user_id = ctx.author.id
    
    if user_id not in user_slimes or not user_slimes[user_id]:
        embed = discord.Embed(description="You haven't caught any slimes yet.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    total_coins = 0
    
    if rarity:
        if rarity.lower() not in rarities:
            embed = discord.Embed(description="Invalid rarity specified.", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        
        slimes_to_sell = [slime for slime in user_slimes[user_id] if slime["rarity"] == rarity.lower()]
        
        if not slimes_to_sell:
            embed = discord.Embed(description=f"You don't have any {rarity.capitalize()} slimes to sell.", color=0xFF0000)
            await ctx.send(embed=embed)
            return
        
        for slime in slimes_to_sell:
            total_coins += rarities[slime["rarity"]]["value"]
        
        user_slimes[user_id] = [slime for slime in user_slimes[user_id] if slime not in slimes_to_sell]
    else:
        slimes_to_sell = user_slimes[user_id]
        for slime in slimes_to_sell:
            total_coins += rarities[slime["rarity"]]["value"]
        user_slimes[user_id] = []
    
    if user_id not in user_balances:
        user_balances[user_id] = 0
    user_balances[user_id] += total_coins
    
    rarity_name = rarity.capitalize() if rarity else "All"
    embed = discord.Embed(description=f"All {rarity_name} slimes have been sold for a total of {total_coins} coins! Your new balance is {user_balances[user_id]} coins.", color=0x00FF00)
    await ctx.send(embed=embed)

@bot.command()
async def shop(ctx):
    embed = discord.Embed(title="Shop", color=0x00FFFF)
    for item in cosmetic_items:
        embed.add_field(name=item["name"], value=f"Rarity: {item['rarity']}, Price: {item['price']} coins", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def buy(ctx, *, item_name: str):
    user_id = ctx.author.id

    item = next((x for x in cosmetic_items if x["name"].lower() == item_name.lower()), None)
    if not item:
        await ctx.send("Item not found in the shop.")
        return

    user_balance = user_balances.get(user_id, 0)
    if user_balance < item["price"]:
        await ctx.send("You don't have enough coins to purchase this item.")
        return

    user_balances[user_id] -= item["price"]

    if user_id not in user_items:
        user_items[user_id] = []
    user_items[user_id].append(item)
    
    await ctx.send(f"You have purchased {item['name']} for {item['price']} coins.")

@bot.command()
async def inv(ctx):
    user_id = ctx.author.id
    
    if user_id not in user_items or not user_items[user_id]:
        embed = discord.Embed(description="No items yet! Use ?shop to purchase.", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(title=f"{ctx.author.display_name}'s Items", color=0x00FF00)
    for item in user_items[user_id]:
        embed.add_field(name=item["name"], value=f"Rarity: {item['rarity']}", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def gamble(ctx, amount: int = None):
    user_id = ctx.author.id
    user_balance = user_balances.get(user_id, 0)
    
    if amount is None:
        amount = user_balance
    
    if amount <= 0:
        await ctx.send("Please enter a positive amount to gamble.")
        return
    
    if amount > user_balance:
        embed = discord.Embed(description=f"Sorry {ctx.author.mention}, you don't have enough coins to play!", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    outcome = random.choices(["win", "lose", "no_change"], weights=[0.33, 0.33, 0.34])[0]
    
    embed = discord.Embed(title="Gambling...", color=0x00FFFF)
    message = await ctx.send(embed=embed)
    
    await asyncio.sleep(3)
    
    if outcome == "win":
        user_balances[user_id] += amount
        embed = discord.Embed(title="You won! 🥳", description=f"Your balance: {user_balances[user_id]} coins", color=0x00FF00)
    elif outcome == "lose":
        user_balances[user_id] -= amount
        embed = discord.Embed(title="You lost! 😡", description=f"Your balance: {user_balances[user_id]} coins", color=0xFF0000)
    else:
        embed = discord.Embed(title="No change...", description=f"Your balance: {user_balances[user_id]} coins", color=0xFFFF00)
    
    await message.edit(embed=embed)

@bot.command()
async def duel(ctx, user: discord.Member = None, amount: int = None):
    user_id = ctx.author.id
    target_id = user.id

    if target_id not in user_slimes or not user_slimes[target_id]:
        embed = discord.Embed(description="You need slimes to duel!", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    if user is None:
        embed = discord.Embed(description="No user specified!", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    if amount is None:
        embed = discord.Embed(description="Specify an amount!", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    if amount > user_balances.get(user_id, 0):
        embed = discord.Embed(description="You don't have enough coins to duel!", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    await ctx.send(f"{user.mention}, {ctx.author.display_name} has challenged you to a duel for {amount} coins! Type ?duelacc to accept, or ?duelrjt to reject.")
    duel_request = (ctx.author.id, user.id, amount)
    duel_requests[user.id] = duel_request

@bot.command()
async def duelacc(ctx):
    user_id = ctx.author.id
    duel_request = duel_requests.pop(user_id, None)
    
    if duel_request is None:
        embed = discord.Embed(description="No valid duel!", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    challenger_id, target_id, amount = duel_request
    challenger_balance = user_balances.get(challenger_id, 0)
    target_balance = user_balances.get(target_id, 0)
    
    if amount > target_balance:
        embed = discord.Embed(description=f"{ctx.author.display_name} doesn't have enough coins to duel!", color=0xFF0000)
        await ctx.send(embed=embed)
        return
    
    await ctx.send(f"{ctx.author.mention} has accepted the duel!")

    challenger_slimes = user_slimes.get(challenger_id, [])
    target_slimes = user_slimes.get(target_id, [])
    
    challenger_rarity_count = Counter(slime["rarity"] for slime in challenger_slimes)
    target_rarity_count = Counter(slime["rarity"] for slime in target_slimes)
    
    challenger_highest_rarity = max(challenger_rarity_count, default="", key=lambda x: rarities.get(x, {}).get("weight", 0))
    target_highest_rarity = max(target_rarity_count, default="", key=lambda x: rarities.get(x, {}).get("weight", 0))

    if rarities.get(challenger_highest_rarity, {}).get("weight", 0) > rarities.get(target_highest_rarity, {}).get("weight", 0):
        winner_id = challenger_id
        loser_id = target_id
    elif rarities.get(challenger_highest_rarity, {}).get("weight", 0) < rarities.get(target_highest_rarity, {}).get("weight", 0):
        winner_id = target_id
        loser_id = challenger_id
    else:
        winner_id = random.choice([challenger_id, target_id])
        loser_id = challenger_id if winner_id == target_id else target_id

    user_balances[winner_id] += amount
    user_balances[loser_id] -= amount

    winner_name = ctx.author.display_name if winner_id == ctx.author.id else await bot.fetch_user(winner_id)
    loser_name = ctx.author.display_name if loser_id == ctx.author.id else await bot.fetch_user(loser_id)
    
    embed = discord.Embed(title="Dueling...", color=0xFFFF00)
    message = await ctx.send(embed=embed)
    
    await asyncio.sleep(5)

    embed.title = "Duel Result"
    if winner_id == challenger_id:
        embed.description = f"{winner_name} won the duel and received {amount} coins from {loser_name}!"
    else:
        embed.description = f"{loser_name} won the duel and received {amount} coins from {winner_name}!"
    await message.edit(embed=embed)

@bot.command()
async def duelrjt(ctx):
    challenger_id = ctx.author.id

    if challenger_id not in duel_requests:
        embed = discord.Embed(description="No valid duel!", color=0xFF0000)
        await ctx.send(embed=embed)
        return

    challenger_id, target_id, amount = duel_requests.pop(challenger_id)
    
    embed = discord.Embed(description=f"Duel from <@{challenger_id}> rejected!", color=0x00FF00)
    await ctx.send(embed=embed)

@bot.command()
async def schelp(ctx):
    embed = discord.Embed(title="Help", color=0x00FF00)
    embed.add_field(name="?catch", value="Catch a slime.", inline=False)
    embed.add_field(name="?slimes", value="View your caught slimes.", inline=False)
    embed.add_field(name="?duel [user] [amount]", value="Challenge a user to a duel.", inline=False)
    embed.add_field(name="?duelacc", value="Accept a duel challenge.", inline=False)
    embed.add_field(name="?duelrjt", value="Reject a duel challenge.", inline=False)
    embed.add_field(name="?bal", value="View your current balance.", inline=False)
    embed.add_field(name="?sellall [rarity]", value="Sell all slimes in your inventory. Optionally, specify a rarity to sell only slimes of that rarity.", inline=False)
    embed.add_field(name="?shop", value="View the shop.", inline=False) 
    embed.add_field(name="?buy [item_name]", value="Buy an item from the shop.", inline=False)
    embed.add_field(name="?inv", value="View your items.", inline=False)
    embed.add_field(name="?gamble [amount]", value="Gamble coins. Optionally, specify an amount to gamble.", inline=False)
    embed.add_field(name="?schelp", value="Display this help message.", inline=False)
    
    await ctx.send(embed=embed)

# Admin commands

@bot.command()
async def setbal(ctx, amount: int, user: discord.Member = None):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("Insufficient permissions.")
        return
    
    if user is None:
        user = ctx.author
    
    user_id = user.id
    user_balances[user_id] = amount

    await ctx.send(f"Successfully set {user.display_name}'s balance to {amount} coins.")

@bot.command()
async def resetbal(ctx, user: discord.Member = None):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("Insufficient permissions.")
        return
    
    if user is None:
        user = ctx.author
    
    user_id = user.id
    user_balances.pop(user_id, None)

    await ctx.send(f"Successfully reset {user.display_name}'s balance.")

bot.run(BOT_TOKEN)