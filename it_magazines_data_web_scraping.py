'''
it magazines web scraping
'''

import json
import re
from dataclasses import dataclass, field, asdict
from enum import Enum
import requests
from bs4 import BeautifulSoup, Tag

class ItMagazineType(Enum):
    '''
    magazine type
    '''
    # 技術評論社
    SOFTWARE_DESIGN = 1
    WEB_DB_PRESS = 2
    # CQ出版
    INTERFACE = 11
    TRANGISTOR_GIJUTSU = 12

@dataclass
class ItMagazineTopoutlineData:
    '''
    magazine top-outline data class
    '''
    category: str = ''
    title: str = ''
    catch: str = ''

@dataclass
class ItMagazineData:
    '''
    magazine data class
    '''
    name: str
    number: str = ''
    price: str = ''
    release_date: str = ''
    top_outlines: list[ItMagazineTopoutlineData] = field(default_factory=list)

    def get_dict(self):
        '''
        get dict data
        '''
        return asdict(self)

    def get_json(self):
        '''
        get json data
        '''
        return json.dumps(self.get_dict(), indent=2, ensure_ascii=False)

def __get_soup(url: str) -> BeautifulSoup:
    '''
    get soup data from url
    '''
    html = requests.get(url, timeout=(3.0, 10.0))
    return BeautifulSoup(html.content, 'html.parser')

def __scrape_software_design():
    magazine_data = ItMagazineData(name='Software Design')

    soup = __get_soup('http://gihyo.jp/magazine/SD')
    tag_salesinfo1 = soup.find('div', id='newPublishedInfo')
    tag_salesinfo2: Tag = None
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('a', string=re.compile('月号'))
        magazine_data.number\
            = _number.get_text(strip=True) if _number is not None else ''
        tag_salesinfo2 = tag_salesinfo1.find('div', class_='information')
    if tag_salesinfo2 is not None:
        _release_date = tag_salesinfo2.find(string=re.compile('発売'))
        magazine_data.release_date\
            = _release_date.get_text(strip=True) if _release_date is not None else ''
        _price = tag_salesinfo2.find(string=re.compile('定価'))
        magazine_data.price = _price.get_text(strip=True) if _price is not None else ''

    tag_topoutline = soup.find('div', id='magazineTopOutline')
    if tag_topoutline is not None:
        for tag_li in tag_topoutline.find_all('li'):
            _category = tag_li.find('span', class_='category')
            _title = tag_li.find('span', class_='title')
            _catch = tag_li.find('span', class_='catch')
            magazine_data.top_outlines.append(
                ItMagazineTopoutlineData(
                    category=_category.get_text(strip=True) if _category is not None else '',
                    title=_title.get_text(strip=True) if _title is not None else '',
                    catch=_catch.get_text(strip=True) if _catch is not None else ''
                )
            )
    return magazine_data

def __scrape_web_db_press() -> ItMagazineData:
    magazine_data = ItMagazineData(name='WEB+DB PRESS')

    soup = __get_soup('https://gihyo.jp/magazine/wdpress')
    tag_salesinfo1 = soup.find('div', id='newPublishedInfo')
    tag_salesinfo2: Tag = None
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('a', string=re.compile('Vol.'))
        magazine_data.number\
            = _number.get_text(strip=True) if _number is not None else ''
        tag_salesinfo2 = tag_salesinfo1.find('div', class_='information')
    if tag_salesinfo2 is not None:
        _release_date = tag_salesinfo2.find(string=re.compile('発売'))
        magazine_data.release_date\
            = _release_date.get_text(strip=True) if _release_date is not None else ''
        _price = tag_salesinfo2.find(string=re.compile('定価'))
        magazine_data.price = _price.get_text(strip=True) if _price is not None else ''

    tag_topoutline = soup.find('div', id='magazineTopOutline')
    if tag_topoutline is not None:
        for tag_li in tag_topoutline.find_all('li'):
            _category = tag_li.find('span', class_='category')
            _title = tag_li.find('span', class_='title')
            _catch = tag_li.find('span', class_='catch')
            magazine_data.top_outlines.append(
                ItMagazineTopoutlineData(
                    category=_category.get_text(strip=True) if _category is not None else '',
                    title=_title.get_text(strip=True) if _title is not None else '',
                    catch=_catch.get_text(strip=True) if _catch is not None else ''
                )
            )
    return magazine_data

def __scrape_interface() -> ItMagazineData:
    magazine_data = ItMagazineData(name='Interface')

    # search book page link
    soup = __get_soup('https://interface.cqpub.co.jp/')
    tag_link = soup.find('div', class_='latest-info')
    if tag_link is not None:
        tag_link = tag_link.find('a')
    if tag_link is not None:
        _link = tag_link.get('href')
    if _link is None:
        return magazine_data
    # scrape page
    soup2 = __get_soup(_link)
    tag_salesinfo1 = soup2.find('div', class_='latest-info')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('h2')
        magazine_data.number\
            = _number.get_text(strip=True) if _number is not None else ''
        _price = tag_salesinfo1.find(class_='price')
        magazine_data.price = _price.get_text(strip=True) if _price is not None else ''

    for tag_h3 in soup2.find_all('h3', class_='title01'):
        magazine_data.top_outlines.append(
            ItMagazineTopoutlineData(
                title=tag_h3.get_text(strip=True) if tag_h3 is not None else ''
            )
        )
    return magazine_data

def __scrape_trangistor_gijutsu() -> ItMagazineData:
    magazine_data = ItMagazineData(name='トランジスタ技術')

    # search book page link
    soup = __get_soup('https://toragi.cqpub.co.jp/')
    tag_link = soup.find('section', id='sec01')
    if tag_link is not None:
        tag_link = tag_link.find('div', class_='book')
    if tag_link is not None:
        tag_link = tag_link.find('a')
    if tag_link is not None:
        _link = tag_link.get('href')
    if _link is None:
        return magazine_data
    # scrape page
    soup2 = __get_soup(_link)
    tag_salesinfo1 = soup2.find('div', class_='latest-info')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('h2', class_='book-title')
        magazine_data.number\
            = _number.get_text(strip=True) if _number is not None else ''
        _price = tag_salesinfo1.find('div', class_='issue-date')
        magazine_data.price = _price.get_text(strip=True) if _price is not None else ''

    for tag_li in tag_salesinfo1.find_all('dl', class_=['tokushu', 'furoku']):
        _category = tag_li.find('dt')
        _title = tag_li.find('dd')
        magazine_data.top_outlines.append(
            ItMagazineTopoutlineData(
                category=_category.get_text(strip=True) if _category is not None else '',
                title=_title.get_text(strip=True) if _title is not None else ''
            )
        )
    return magazine_data

def scrape_magazine(magazine_type: ItMagazineType) -> ItMagazineData:
    '''
    run web scraping
    '''
    if magazine_type == ItMagazineType.SOFTWARE_DESIGN:
        return __scrape_software_design()
    if magazine_type == ItMagazineType.WEB_DB_PRESS:
        return __scrape_web_db_press()
    if magazine_type == ItMagazineType.INTERFACE:
        return __scrape_interface()
    if magazine_type == ItMagazineType.TRANGISTOR_GIJUTSU:
        return __scrape_trangistor_gijutsu()
    return None

if __name__ == '__main__':
    print(scrape_magazine(ItMagazineType.SOFTWARE_DESIGN).get_json())
    print(scrape_magazine(ItMagazineType.WEB_DB_PRESS).get_json())
    print(scrape_magazine(ItMagazineType.INTERFACE).get_json())
    print(scrape_magazine(ItMagazineType.TRANGISTOR_GIJUTSU).get_json())
