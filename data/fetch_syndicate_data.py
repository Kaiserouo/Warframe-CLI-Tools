from lxml import etree
import requests
syndicates = [
    {
        'name': 'Cavia',
        'url': 'https://warframe.fandom.com/wiki/Cavia',
        'sections': [
            {'selector': "//*[@id='mw-customcollapsible-bird3wares']/div[1]/div//a/span/text()"}
        ],
  },
]

def default_mapper():
    pass

def get_syndicate_items(syndicate: dict) -> dict[str, list[str]]:
    """
        must have 'name', 'url', 'sections'
    """
    r = requests.get(syndicate['url'])
    html = etree.HTML(r.content)
    names = html.xpath(syndicate['sections'][0]['selector'])
    return names

print({
    syndicate['name']: get_syndicate_items(syndicate)
    for syndicate in syndicates
})