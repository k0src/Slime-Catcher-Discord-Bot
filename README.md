# Slime Catcher

Slime Catcher is an open-source fun Discord bot template where you can catch, breed, and duel with slimes!

![Main Gif](/assets/main.gif)

## Features
- **Rare Slimes**: Catch rare slimes with unique colors and attributes.
- **Dueling System**: Challenge your friends to duels and win coins!
- **Currency System**: Earn coins by winning duels or selling slimes in the shop.
- **Gambling**: Take a chance to gamble all or a bit of your money, for a chance to double it, or lose all of it.
- **Shop**: Spend your hard-earned coins on various items and upgrades.
- **Inventory Management**: Keep track of all your slimes and items in your inventory.
- **Randomly Generated Slimes**: Encounter a wide variety of randomly generated slimes.

## Usage
### Commands
- `?catch`: Catch a random slime.
- `?slimes`: View your slimes.
- `?duel <user> <amount>`: Challenge another user to a duel for a specified amount of coins.
    - `?duelacc` or `?duelrjt` to accept or reject the duel.
- `?bal`: Check your current balance.
- `?sell all [rarity]`: Sell all slimes in your inventory. Optionally, specify a rarity to sell only slimes of that rarity.
- `gamble [amount]`: Gamble coins. Optionally, specify an amount to gamble.
- `?shop`: View available items in the shop.
    - `?buy`: Buy an item from the shop.
- `?inventory`: View your inventory of items.
- `?schelp`: Display the help menu.

### Admin Commands:
- `?setbal`: Set the balance of a user.
- `?resetbal`: Reset the balance of a user.

## Installation Guide

![Install Gif](/assets/install.gif)

Create a Discord Developers account [here](https://discord.com/developers/).

1. Clone this repo: `git clone git@github.com:k0src/Slime-Catcher-Discord-Bot.git`.
2. Select "Create New Application", give the bot permissions, set the profile picture and name, and create an OAUTH link.
3. Replace `BOT_TOKEN` with your bot token, and `ADMIN_ID` with your [Discord ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID).
4. Paste the OAUTH link into your browser, and invite the bot to your server.
5. Edit `slimecatcher.py` to add or change any attributes about the bot.

Have fun!