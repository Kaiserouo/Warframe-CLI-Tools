from dataclasses import dataclass
import json
import re

import requests
from joblib import Parallel, delayed
import time
import random
import datetime
import math
import itertools
import statistics

import util
from tqdm import tqdm

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

def retry_request(*args, **kwargs):
    """
        automatically retry request until the request is done.
        this is to retry whenever too many requests happens
    """
    while True:
        r = requests.get(*args, **kwargs)

        if r.status_code == 200:
            break

        # wait a random time because there may be multiple requests
        # at the exact same time as this
        time.sleep(random.uniform(0, 1))    
    return r

class Orders:
    """
        existing orders on warframe market
    """

    @dataclass
    class Order():
        order_type: str
        visible: bool
        platinum: int
        quantity: int
        user_reputation: int
        user_status: str
        mod_rank: int

        @property
        def is_sell(self):
            return self.order_type == 'sell'
        
        @property
        def is_buy(self):
            return self.order_type == 'buy'
        
        @property
        def is_ingame(self):
            return self.user_status == 'ingame'

    def __init__(self, order_json):
        """
            order_json: is a list of dict that has keys like [visible, user, quantity, ...] 
        """

        self.orders: list[self.Order] = []
        for order in order_json:
            cur_order = self.Order(**{
                'order_type': order['order_type'],
                'visible': order['visible'],
                'platinum': order['platinum'],
                'quantity': order['quantity'],
                'user_reputation': order['user']['reputation'],
                'user_status': order['user']['status'], # can be ['offline', 'online', 'ingame']
                'mod_rank': order.get('mod_rank', 0)
            })
            self.orders.append(cur_order)
            
    def get_ingame_lowest_sell_price(self, mod_rank_range: list | range = [0]):
        return min([
            order.platinum for order in self.orders
            if order.is_sell and order.visible and order.is_ingame and order.mod_rank in mod_rank_range 
        ] + [1000000])
    def get_ingame_highest_buy_price(self, mod_rank_range: list | range = [0]):
        return max([
            order.platinum for order in self.orders
            if order.is_buy and order.visible and order.is_ingame and order.mod_rank in mod_rank_range 
        ] + [-1])
    def get_ingame_bottomK_sell_price(self, k: int, mod_rank_range: list | range = [0]):
        sell_list = sorted([
            (order.platinum, order.quantity) for order in self.orders
            if order.is_sell and order.visible and order.is_ingame and order.mod_rank in mod_rank_range 
        ])
        return sell_list[:k]
    def get_ingame_topK_buy_price(self, k: int, mod_rank_range: list | range = [0]):
        buy_list = sorted([
            (order.platinum, order.quantity) for order in self.orders
            if order.is_buy and order.visible and order.is_ingame and order.mod_rank in mod_rank_range 
        ], reverse=True)
        return buy_list[:k]

class Statistic:
    """
        statistics for the past 48hr / 90days on warframe market
    """
    def __init__(self, statistic_json: dict, basis_time: datetime.datetime | None = None):
        """
            statistic_json: 
                a dict that has keys [statistics_closed, statistics_opened]
                meaning the deals closed / opened at that timeslot

                they both has heys [48hours, 90days], with each item as a timeslot
                of an hour and a day.

                for statistics_closed (i.e., the price chart on warframe.market),
                it has something like this:
                {
                    "datetime": "2024-07-29T07:00:00.000+00:00",    # that timepoint
                    "volume": 1, # the volume at the bottom of the chart
                    "min_price": 15,  # for candle chart
                    "max_price": 15,
                    "open_price": 15,
                    "closed_price": 15,
                    "avg_price": 15.0,  # for average chart
                    "wa_price": 15.0,  # (idk, is this even on the chart)
                    "median": 15,   # median / blue line
                    "moving_avg": 12.8,  # SMA / black line
                    "donch_top": 15,  # the grey area in the chart
                    "donch_bot": 10,
                    "id": "66a74c44bba77400155161b8",
                    "mod_rank": a number
                },
                note that the json MIGHT sort timeslot in ascending order so...take note of that
                the 90days timeslot will only record up until the last time 00:00 UTC happens
                so might not be the exact newest data (with data age at most 24 hours)
        """

        # TODO: deal with statistics
        self.statistics = statistic_json.copy()
        self.basis_time = basis_time

        # change datetime into actual datetime object
        for stat_type in self.statistics:
            for timeframe_type in self.statistics[stat_type]:
                for stat in self.statistics[stat_type][timeframe_type]:
                    stat['datetime'] = datetime.datetime.fromisoformat(stat['datetime'])
                    stat['mod_rank'] = stat.get('mod_rank', 0)

    """
        Statistic filtering, should be given **stat_filter:
            - basis_time: we filter the timestamp by going back N hours / days from the basis time. 
                          we define the basis time (that we calculate the "last N hours" for) as:
                            - basis_time, if it is not None.
                            - self.basis_time, if it is not None.
                            - datatime.datetime.now()
            - mod_rank_range: the mod rank range we wanna filter the statistic for
                              if it is not a mod then its rank is 0 (which is the default option,
                              you don't need to give this filter in that case).
                              theoretically should only have 2 options: 0 and max rank, but due to
                              future proof and the fact that i don't know what an item's max rank is,
                              you can set this as [0] or range(1, 100) to filter these 2 cases for now 
                              (or range(100) if you specifically want all the mod ranks)
    """

    def get_stat_for_last_hours(self, hours: int, 
                                basis_time: datetime.datetime | None = None,
                                mod_rank_range: list | range = [0]):
        """
            get the closed trade stat for the last {hours} hours
            hours in range [1, 48], might not be up to 48 because it depends on
            how many timeslots the API sends back for 48hours.
            
            there must be some error because the records is made on the hour

            may return empty list
        """
        if basis_time is None:
            if self.basis_time is None:
                basis_time = datetime.datetime.now(datetime.timezone.utc)
            else:
                basis_time = self.basis_time

        valid_stat = [
            stat for stat in self.statistics['statistics_closed']['48hours']
            if stat['datetime'] > basis_time - datetime.timedelta(hours=hours)
            and stat['mod_rank'] in mod_rank_range
        ]

        return valid_stat

    def get_stat_for_last_days(self, days: int, 
                               basis_time: datetime.datetime | None = None,
                               mod_rank_range: list | range = [0]):
        """
            get the closed trade stat for the last {days} days
            days in range [1, 90], might not be up to 90 because it depends on
            how many timeslots the API sends back for 90days.

            the records are made on the day in UTC

            some details refer to get_volume_for_last_hours
            may return empty list
        """
        if basis_time is None:
            if self.basis_time is None:
                basis_time = datetime.datetime.now(datetime.timezone.utc)
            else:
                basis_time = self.basis_time

        valid_stats = [
            stat for stat in self.statistics['statistics_closed']['90days']
            if stat['datetime'] > basis_time - datetime.timedelta(days=days)
            and stat['mod_rank'] in mod_rank_range
        ]

        return valid_stats

    """
        The actual statistic calculation part.
        Can give kwarg **stat_filter to use the above stat, or if there isn't any,
        it should do the filtering itself.
        Must handle the case where get_stat_for_last_*() returns an empty list
    """

    def get_volume_for_last_hours(self, hours: int, **stat_filter):
        """
            get the closed trade volume for the last {hours} hours
            hours in range [1, 48], might not be up to 48 because it depends on
            how many timeslots the API sends back for 48hours.
            
            there must be some error because the records is made on the hour
        """
        stats = self.get_stat_for_last_hours(hours, **stat_filter)
        return sum([stat['volume'] for stat in stats])
    
    def get_volume_for_last_days(self, days: int, **stat_filter):
        """
            get the closed trade volume for the last {days} days
            days in range [1, 90], might not be up to 90 because it depends on
            how many timeslots the API sends back for 90days.

            the records are made on the day in UTC

            some details refer to get_volume_for_last_hours
        """
        stats = self.get_stat_for_last_days(days, **stat_filter)
        return sum([stat['volume'] for stat in stats])

class PriceOracle:
    """
        calculate the price for the given item
    """
    def __init__(self, item, orders: Orders, statistic: Statistic):
        self.item = item
        self.orders = orders
        self.statistic = statistic
    
    def get_avg_median_price_for_last_hours(self, hours: int, ratio: float = 1, **stat_filter):
        """
            don't take the volume into account, everything is based on medians in a timeframe
            ratio: pick the top `ratio` median prices to calculate average, 
        """
        stats = self.statistic.get_stat_for_last_hours(hours, **stat_filter)
        if len(stats) == 0:
            return 0
        medians = [stat['median'] for stat in stats]
        top_medians = sorted(medians, reverse=True)[:int(len(medians) * ratio)]
        if len(medians) == 0:
            return sum(medians) / len(medians)
        return sum(top_medians) / len(top_medians)
    
    def get_avg_median_price_for_last_days(self, days: int, **stat_filter):
        stats = self.statistic.get_stat_for_last_days(days, **stat_filter)
        if len(stats) == 0:
            return 0
        return sum([stat['median'] for stat in stats]) / len(stats)
    
    def get_top_k_median_price_for_last_hours(self, hours: int, ratio: float = 1, **stat_filter):
        """
            actually take the volume into account
            ratio: pick the top `ratio` prices to calculate average
        """
        stats = self.statistic.get_stat_for_last_hours(hours, **stat_filter)
        if len(stats) == 0:
            return 0
        
        prices = [[stat['median']] * stat['volume'] for stat in stats]
        prices = list(itertools.chain.from_iterable(prices))
        prices = sorted(prices, reverse=True)

        top_K = prices[:int(len(prices) * ratio)]
        if len(top_K) == 0:
            return statistics.median(prices)
        return statistics.median(top_K)
    
    def get_top_k_avg_price_for_last_hours(self, hours: int, ratio: float = 1, **stat_filter):
        """
            actually take the volume into account
            ratio: pick the top `ratio` prices to calculate average
        """
        stats = self.statistic.get_stat_for_last_hours(hours, **stat_filter)
        if len(stats) == 0:
            return 0
        
        prices = [[stat['median']] * stat['volume'] for stat in stats]
        prices = list(itertools.chain.from_iterable(prices))
        prices = sorted(prices, reverse=True)

        top_K = prices[:int(len(prices) * ratio)]
        if len(top_K) == 0:
            return statistics.mean(prices)
        return statistics.mean(top_K)

    def get_oracle_price_48hrs(self, **stat_filter):
        """
            For the best price that probably applies to everything
            must be prepare()-ed first
        """
        # return self.get_avg_median_price_for_last_hours(48, 0.5, **stat_filter)
        # return self.get_top_k_avg_price_for_last_hours(48, 0.3, **stat_filter)
        price = self.get_top_k_avg_price_for_last_hours(3, 1, **stat_filter)
        if price > 0: return price

        price = self.get_top_k_avg_price_for_last_hours(48, 0.3, **stat_filter)
        if price > 0: return price

        return self.orders.get_ingame_topK_buy_price(5, mod_rank_range=stat_filter.get('mod_rank_range', [0]))

class MarketItem:
    def __init__(self, market_json: dict, api_version: str = 'v1'):
        """
            market_json: differs according to API version 
                'v1': has keys like ['id', 'url_name', 'thumb', 'item_name']
                'v2': {
                    gameRef: "/Lotus/Powersuits/Ember/FireBlastAugmentCard"
                    i18n: {en: {name: "Healing Flame",…}}
                        en: {name: "Healing Flame",…}
                            name: "Healing Flame"
                            thumb: "items/images/en/thumbs/healing_flame.0672e5552e12d348dbc0521e3841c9a1.128x128.png"
                    id: "54e0c9eee7798903744178ae"
                    tags: []
                    urlName: "healing_flame"
                    maxRank: 3  # may appear
                }

            accessible traits:
                - id, url_name, thumb, item_name: accessible
                - orders, statistics: need to prepare() first, else None
                - is_mod_info_available: accessible, and if True:
                    - is_mod: accessible
                    - mod_max_rank: accessible, 0 if not is_mod 
        """
        if api_version == 'v1':
            self.id = market_json['id']
            self.url_name = market_json['url_name']
            self.thumb = market_json['thumb']
            self.item_name = market_json['item_name']
            self.orders: Orders | None = None
            self.statistic: Statistic | None = None
            self.price: PriceOracle | None = None
            self.is_mod_info_available = False
        
        elif api_version == 'v2':
            self.id = market_json['id']
            self.url_name = market_json['urlName']
            self.thumb = market_json['i18n']['en'].get('thumb', None)
            self.item_name = market_json['i18n']['en']['name']
            self.orders = None
            self.statistic = None
            self.price = None
            self.is_mod_info_available = True
            self.is_mod = ('maxRank' in market_json)
            self.mod_max_rank = market_json.get('maxRank', 0)

    def _get_orders(self):
        r = retry_request(f'https://api.warframe.market/v1/items/{self.url_name}/orders', headers={
            'accept': 'application/json',
            'Platform': 'pc',
            'User-agent': USER_AGENT
        })

        return Orders(json.loads(r.content)['payload']['orders'])

    def _get_statistic(self):
        r = retry_request(f'https://api.warframe.market/v1/items/{self.url_name}/statistics', headers={
            'accept': 'application/json',
            'Platform': 'pc',
            'User-agent': USER_AGENT
        })

        return Statistic(json.loads(r.content)['payload'])
    
    def prepare(self):
        """
            fetch anything it can first and store inside itself
            please don't get_order or get_statistics yourself
        """
        self.orders = self._get_orders()
        self.statistic = self._get_statistic()
        self.price = PriceOracle(self, self.orders, self.statistic)

        return self.orders, self.statistic, self.price

    def get_wfm_url(self):
        """
            make warframe market URL
        """
        return f"https://warframe.market/items/{self.url_name}"

    def __str__(self):
        return f'<MarketItem "{self.item_name}">'
    def __repr__(self):
        return f'<MarketItem "{self.item_name}">'

def get_market_item_list() -> list[MarketItem]:
    r = retry_request('https://api.warframe.market/v2/items', headers={
        'accept': 'application/json',
        'Language': 'en',
        'User-agent': USER_AGENT
    })
    # items = json.loads(r.content)['payload']['items']   # for v1
    items = json.loads(r.content)['data']
    return [MarketItem(i, api_version='v2') for i in items]

def prepare_market_items(market_items: list[MarketItem]):
    "does parallel"
    def task(item: MarketItem):
        item.prepare()
        return item
    
    with util.tqdm_joblib(tqdm(range(len(market_items)), 'Fetching items...')) as tqdm_progress:
        results = Parallel(n_jobs=5, require='sharedmem')(delayed(task)(item) for item in market_items)

    for i in range(len(market_items)):
        market_items[i] = results[i]
        
def get_syndicate_items(syndicate_name: str, market_map: None | list[MarketItem] = None) -> list[MarketItem]:
    """
        e.g., [
            "Arbiters of Hexis", "Steel Meridian", "The Quills", "NecraLoid", "Vox Solaris", "Ventkids", 
            "Cephalon Simaris", "New Loka", "Cephalon Suda", "Red Veil", "The Perrin Sequence", 
            "Solaris United", "Entrati", "Ostron", "The Holdfasts", "Kahl's Garrison", "Operational Supply", 
            "Conclave",
        ] + ['Cavia']

        ref. https://github.com/WFCD/warframe-drop-data
    """
    from data.syndicate_data import additional_syndicates
    if market_map is None:
        market_map = get_market_items_name_map()

    syndicate_item_names: list[str] = None
    if syndicate_name in additional_syndicates:
        syndicate_item_names = additional_syndicates[syndicate_name]['names']
    else:
        r = requests.get('https://drops.warframestat.us/data/syndicates.json')
        syndicate_item_names = json.loads(r.content)['syndicates'][syndicate_name]
        syndicate_item_names = [i['item'] for i in syndicate_item_names]
    
    # deal with warframe mods that has trailing names and parenthesis in them
    parenthesis_item_names = [
        name[:name.index('(') - 1]
        for name in syndicate_item_names if '(' in name
    ]
    syndicate_item_names = set(syndicate_item_names) | set(parenthesis_item_names)

    syndicate_item_names = syndicate_item_names & set(market_map.keys())

    return [market_map[name] for name in syndicate_item_names]

def get_market_items_name_map(market_items: None | list[MarketItem] = None) -> dict[str, MarketItem]:
    if market_items is None:
        market_items = get_market_item_list()
    return {i.item_name: i for i in market_items}

def get_relic_data(discard_forma: bool = False) -> dict[str, dict[str, list[str]]]:
    """
        only fetch from drops.warframestat.us
        if you have any other manually recorded data then do it on your own

        discard_forma: doesn't contain forma information if true

        return {relic name -> {rarity: list of items}}
    """
    r = retry_request('https://drops.warframestat.us/data/relics.json')
    relic_data_ls = json.loads(r.content)['relics']
    relic_map = {}
    for relic_data in relic_data_ls:
        if relic_data['state'] != 'Intact':
            continue    # we only want the list of items

        relic = {"Common": [], "Uncommon": [], "Rare": []}
        for reward in relic_data['rewards']:
            if discard_forma and 'Forma Blueprint' in reward['itemName']:
                continue
            
            # filter by chance: [25.33, 11, 2], use 20, 5 as a bound
            if reward['chance'] > 20:
                relic['Common'].append(reward['itemName'])
            elif reward['chance'] > 5:
                relic['Uncommon'].append(reward['itemName'])
            else:
                relic['Rare'].append(reward['itemName'])
        relic_map[f"{relic_data['tier']} {relic_data['relicName']}"] = relic

    return relic_map