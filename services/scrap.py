import lxml.html
import re

def scrap_leek_crawl(crawl):
    html = lxml.html.fromstring(crawl)

    farmer_id, farmer_name, farmer_team = scrap_farmer(html)
    nb_victory, nb_draw, nb_defeat = scrap_fights(html)

    leek = {
        'name': scrap_name(html),
        'farmer_id': farmer_id,
        'farmer_name': farmer_name,
        'farmer_team': farmer_team,
        'nb_victory': nb_victory,
        'nb_draw': nb_draw,
        'nb_defeat': nb_defeat,
        'level': scrap_level(html),
        'life': scrap_life(html),
        'strength': scrap_strength(html),
        'agility': scrap_agility(html),
        'wisdom': scrap_wisdom(html),
        'frequency': scrap_frequency(html),
        'action_point': scrap_action_point(html),
        'movement_point': scrap_movement_point(html),
        'cores': scrap_cores(html),
        'weapons': scrap_weapons(html),
        'chips': scrap_chips(html)
    }
    return leek

def scrap_name(html):
    xpath = '//*[@id="leek"]/h1/text()'
    return html.xpath(xpath, smart_strings=False)[0]

def scrap_farmer(html):
    xpath = '//*[@id="leek"]/div[1]/a'
    element = html.xpath(xpath)[0]
    text = element.text
    farmer_id = element.attrib['href'].split('/')[-1]
    regex = r'(\[(.+)\] )?(.+)'
    m = re.match(regex, text)
    farmer_name = m.group(3)
    farmer_team = m.group(2)
    return farmer_id, farmer_name, farmer_team

def scrap_level(html):
    xpath = '//*[@id="leek-table"]/tr/td[2]/h2/text()'
    text = html.xpath(xpath, smart_strings=False)[0]
    level = int(text.split(' ')[-1])
    return level

def scrap_fights(html):
    xpath = '//*[@id="fights"]/tr[1]'
    tr = html.xpath(xpath)[0]
    nb_victory = int(''.join(tr.xpath('td[1]/text()')[0].split()))
    nb_draw = int(''.join(tr.xpath('td[2]/text()')[0].split()))
    nb_defeat = int(''.join(tr.xpath('td[3]/text()')[0].split()))
    return nb_victory, nb_draw, nb_defeat

def scrap_life(html):
    xpath = '//*[@id="life"]/text()'
    return int(html.xpath(xpath, smart_string=False)[0])

def scrap_strength(html):
    xpath = '//*[@id="force"]/text()'
    return int(html.xpath(xpath, smart_string=False)[0])

def scrap_agility(html):
    xpath = '//*[@id="agility"]/text()'
    return int(html.xpath(xpath, smart_string=False)[0])

def scrap_wisdom(html):
    xpath = '//*[@id="widsom"]/text()'
    return int(html.xpath(xpath, smart_string=False)[0])

def scrap_frequency(html):
    xpath = '//*[@id="frequency"]/text()'
    return int(html.xpath(xpath, smart_string=False)[0])

def scrap_action_point(html):
    xpath = '//*[@id="tp"]/text()'
    return int(html.xpath(xpath, smart_string=False)[0])

def scrap_movement_point(html):
    xpath = '//*[@id="mp"]/text()'
    return int(html.xpath(xpath, smart_string=False)[0])

def scrap_cores(html):
    xpath = '//*[@id="cores"]/text()'
    return int(html.xpath(xpath, smart_string=False)[0])

def scrap_weapons(html):
    xpath = '//*[@id="leek-weapons"]/*[@class="weapon"]'
    element = html.xpath(xpath)

    def scrap_weapon(div):
        weapons = {
            'pistol': 37,
            'machine_gun': 38,
            'double_gun': 39,
            'shotgun': 41,
            'magnum': 45,
            'laser': 42,
            'grenade_launcher': 43,
            'flame_thrower': 46,
            'destroyer': 40,
            'gazor': 48,
            'b_laser': 60,
            'electrisor': 44,
            'm_laser': 47
        }
        img = div.xpath('img')[0]
        weapon_img = img.attrib['src'].split('/')[-1].split('.')[0]
        return weapons[weapon_img]
    return list(scrap_weapon(e) for e in element)

def scrap_chips(html):
    xpath = '//*[@id="leek-chips"]/*[@class="chip available"]'
    element = html.xpath(xpath)

    def scrap_chip(div):
        chips = {
            'adrenaline': 16,
            'armor': 22,
            'bandage': 3,
            'cure': 4,
            'doping': 26,
            'drip': 10,
            'flame': 5,
            'flash': 6,
            'fortress': 29,
            'helmet': 21,
            'ice': 2,
            'iceberg': 31,
            'leather_boots': 14,
            'liberation': 34,
            'lightning': 33,
            'meteorite': 36,
            'motivation': 15,
            'pebble': 19,
            'protein': 8,
            'rage': 17,
            'rampart': 24,
            'reflexes': 28,
            'resurrection': 35,
            'rock': 7,
            'rockfall': 32,
            'seven_league_boots': 13,
            'shield': 20,
            'shock': 1,
            'spark': 18,
            'stalactite': 30,
            'steroid': 25,
            'stretching': 9,
            'teleportation': 59,
            'vaccine': 11,
            'wall': 23,
            'warm_up': 27,
            'winged_boots': 12,
        }
        img = div.xpath('img')[0]
        chip_img = img.attrib['src'].split('/')[-1].split('.')[0]
        return chips[chip_img]
    return list(scrap_chip(e) for e in element)
