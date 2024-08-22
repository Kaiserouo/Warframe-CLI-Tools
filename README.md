# Warframe CLI Tool

![](./asset/screenshot.png)

I need some functionality that I want full control of, so, um, this.

I parsed some warframe market API (api.warframe.market) related to current price or past statistics so I guess you can yoink my code.

Under constant change and I won't put the newest code up here. You can say it's for record.

## Run

I run python 3.12.3 but i guess you can use a lower version. You can `pip install -r requirements.txt` if you want.

```
python main.py
```

## Functions
Those are what I currently have, as an example of how to use `warframe_market.py`.

```
Function:
- Item Info: Show item info
- Relic Plat: Gives expected plat for specific relic (set)
- Relic Item: Get all relics containing item and give expected plat
- Syndicate: Show syndicate item market price

Note:
- Press TAB to use autocomplete menu, or just type away.
- Use arrow key and press ENTER to choose an item in the menu.
- If not specified, please choose a specific choice (case-sensitive).
- Some functions explicitly shows that it matches ALL items shown in the menu.
  In that case you don't need to choose a specific item. Most of these are case-insensitive, too.
```

## Warning
- Spaghetti code. You can argue I don't have any idea how to structure my code properly. I tried to make it easier to maintain in `warframe_market.py` but i literally just gave up in `interactive.py`.
- **The price oracle (`PriceOracle`) should be changed to fit your needs!** This is the sole reason why I made this whole thing because sometimes alecaframe doesn't show reasonable price and, according to what items I wanna deal with, the price oracle should change accordingly, too. **Don't just use this without knowing what you're doing. At least check if the price oracle fits your needs.**
  - e.g., if an item is common and the price is relatively stable (e.g., equilibrium), I might want to use the median price for the last 48 hours or so.
  - e.g., when a prime is just out (e.g., sevagoth prime as of now), I might only wanna look at the price of the last 3 hours because of how fast the price drops and if i use the price several hours or days ago I am never gonna sell anything.
  - i haven't written the code to choose the price oracle in the CLI for now. please change the code directly. at least im doing it this way for now.
- Mostly useful when you wanna query a lot of items all at once, instead of looking at warframe market page one item at a time.
- A little bit faster than to type the thing on google or warframe market imo, because of the substring matching and stuff.
- Syndicate function can deal with your syndicate standing spending needs if you don't wanna just put all that into relic packs (or, in some syndicate, you can't even buy relic packs so you gotta find something else to sell)
- Relic expected plat calculation is another reason why I made this, because aya relics are not in the database for some reason and alecaframe can't calculate the expected value per relic. I don't have much aya so I'm just gonna calculate that expected price on my own.
- Can also do some weird things that I parsed all warframe market data. Not implemented btw.
  - e.g., auto notify when an item with your expected sell price appears, because I seriously think no one uses the buy function on the market.