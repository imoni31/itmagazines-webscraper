'''
IT-Magazines web scraping
'''

import json
import re
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List
import requests
from bs4 import BeautifulSoup, Tag

class ItMagazineType(Enum):
    '''
    IT-Magazine type
    '''
    # 技術評論社
    SOFTWARE_DESIGN = 1
    WEB_DB_PRESS = 2
    # CQ出版
    INTERFACE = 11
    TRANGISTOR_GIJUTSU = 12
    # 日経BP
    NIKKEI_SOFTWARE = 21
    NIKKEI_LINUX = 22

@dataclass
class ItMagazineStoreLink:
    '''
    IT-Magazine store-link data class
    '''
    name: str = ''
    url: str = ''

@dataclass
class ItMagazineData:
    '''
    IT-Magazine data class
    '''
    name: str
    number: str = ''
    price: str = ''
    release_date: str = ''
    url: str = ''
    top_outlines: List[str] = field(default_factory=list)
    store_links: List[ItMagazineStoreLink] = field(default_factory=list)

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

def __extract_date(_date: Tag) -> str:
    if _date is None:
        return ''
    _date_str = _date.get_text(strip=True)
    res = re.findall(r'\d{4}年\d{1,2}月\d{1,2}日', _date_str)
    if len(res) > 0:
        return res[0]
    res = re.findall(r'\d{1,2}月\d{1,2}日', _date_str)
    if len(res) > 0:
        return res[0]
    res = re.findall(r'\d{4}/\d{1,2}/\d{1,2}', _date_str)
    if len(res) > 0:
        return res[0]
    return ''

def __extract_price(_price: Tag) -> str:
    if _price is None:
        return ''
    _price_str = _price.get_text(strip=True)
    res = re.findall(r'\d{1,3},?\d{1,3}円', _price_str)
    if len(res) > 0:
        return res[0]
    res = re.findall(r'[￥¥]\d{1,3},?\d{1,3}', _price_str)
    if len(res) > 0:
        return res[0]
    return ''

def __scrape_software_design():
    _url = 'http://gihyo.jp/magazine/SD'
    magazine_data = ItMagazineData(name='Software Design', url=_url)

    soup = __get_soup(_url)
    tag_salesinfo1 = soup.find('div', id='newPublishedInfo')
    tag_salesinfo2: Tag = None
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('a', string=re.compile('月号'))
        magazine_data.number\
            = _number.get_text(strip=True) if _number is not None else ''
        tag_salesinfo2 = tag_salesinfo1.find('div', class_='information')
    if tag_salesinfo2 is not None:
        _release_date = tag_salesinfo2.find(string=re.compile('発売'))
        magazine_data.release_date = __extract_date(_date=_release_date)
        _price = tag_salesinfo2.find(string=re.compile('定価'))
        magazine_data.price = __extract_price(_price=_price)

    tag_topoutline = soup.find('div', id='magazineTopOutline')
    if tag_topoutline is not None:
        for tag_li in tag_topoutline.find_all('li'):
            _category = tag_li.find('span', class_='category')
            _title = tag_li.find('span', class_='title')
            magazine_data.top_outlines.append(
                (_category.get_text(strip=True) + ' ' if _category is not None else '')\
                    + (_title.get_text(strip=True) if _title is not None else '')
            )

    tag_storelink = soup.find('dl', class_='storeLink01')
    if tag_storelink is not None:
        for tag_li in tag_storelink.find_all('li'):
            _store_link = tag_li.find('a')
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name=_store_link.get_text(strip=True) if _store_link is not None else '',
                    url=_store_link.get('href') if _store_link is not None else ''
                )
            )
    return magazine_data

def __scrape_web_db_press() -> ItMagazineData:
    _url = 'https://gihyo.jp/magazine/wdpress'
    magazine_data = ItMagazineData(name='WEB+DB PRESS', url=_url)

    soup = __get_soup(_url)
    tag_salesinfo1 = soup.find('div', id='newPublishedInfo')
    tag_salesinfo2: Tag = None
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('a', string=re.compile('Vol.'))
        magazine_data.number\
            = _number.get_text(strip=True) if _number is not None else ''
        tag_salesinfo2 = tag_salesinfo1.find('div', class_='information')
    if tag_salesinfo2 is not None:
        _release_date = tag_salesinfo2.find(string=re.compile('発売'))
        magazine_data.release_date = __extract_date(_date=_release_date)
        _price = tag_salesinfo2.find(string=re.compile('定価'))
        magazine_data.price = __extract_price(_price=_price)

    tag_topoutline = soup.find('div', id='magazineTopOutline')
    if tag_topoutline is not None:
        for tag_li in tag_topoutline.find_all('li'):
            _category = tag_li.find('span', class_='category')
            _title = tag_li.find('span', class_='title')
            magazine_data.top_outlines.append(
                (_category.get_text(strip=True) + ' ' if _category is not None else '')\
                    + (_title.get_text(strip=True) if _title is not None else '')
            )

    tag_storelink = soup.find('dl', class_='storeLink01')
    if tag_storelink is not None:
        for tag_li in tag_storelink.find_all('li'):
            _store_link = tag_li.find('a')
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name=_store_link.get_text(strip=True) if _store_link is not None else '',
                    url=_store_link.get('href') if _store_link is not None else ''
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
        _url = tag_link.get('href')
    if _url is None:
        return magazine_data
    # scrape page
    magazine_data.url = _url
    soup2 = __get_soup(_url)
    tag_salesinfo1 = soup2.find('div', class_='latest-info')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('h2')
        magazine_data.number\
            = _number.get_text(strip=True) if _number is not None else ''
        _price = tag_salesinfo1.find(class_='price')
        magazine_data.release_date = __extract_date(_date=_price)
        magazine_data.price = __extract_price(_price=_price)

    for tag_h3 in soup2.find_all('h3', class_='title01'):
        magazine_data.top_outlines.append(
            tag_h3.get_text(strip=True) if tag_h3 is not None else ''
        )

    _store_link = tag_salesinfo1.find('img', title='書籍の購入')
    if _store_link is not None:
        magazine_data.store_links.append(
            ItMagazineStoreLink(
                name='CQ出版WebShop',
                url=_store_link.parent.get('href') if _store_link is not None else ''
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
        _url = tag_link.get('href')
    if _url is None:
        return magazine_data
    # scrape page
    magazine_data.url = _url
    soup2 = __get_soup(_url)
    tag_salesinfo1 = soup2.find('div', class_='latest-info')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('h2', class_='book-title')
        magazine_data.number\
            = 'トランジスタ技術 ' + _number.get_text(strip=True) if _number is not None else ''
        _price = tag_salesinfo1.find('div', class_='issue-date')
        magazine_data.release_date = __extract_date(_date=_price)
        magazine_data.price = __extract_price(_price=_price)

    for tag_li in tag_salesinfo1.find_all('dl', class_=['tokushu', 'furoku']):
        _category = tag_li.find('dt')
        _title = tag_li.find('dd')
        magazine_data.top_outlines.append(
            (_category.get_text(strip=True) + ' ' if _category is not None else '')\
                + (_title.get_text(strip=True) if _title is not None else '')
        )

    _store_link = tag_salesinfo1.find('a', string='書籍の購入')
    if _store_link is not None:
        magazine_data.store_links.append(
            ItMagazineStoreLink(
                name='CQ出版WebShop',
                url=_store_link.get('href') if _store_link is not None else ''
            )
        )
    return magazine_data

def __scrape_nikkei_software():
    _url = 'https://info.nikkeibp.co.jp/media/NSW/'
    magazine_data = ItMagazineData(name='日経ソフトウエア', url=_url)

    soup = __get_soup(_url)
    tag_salesinfo1 = soup.find('div', class_='articleBody')
    if tag_salesinfo1 is not None:
        tag_salesinfo1 = tag_salesinfo1.find('div', class_='cover-txt')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('p', class_='Title')
        magazine_data.number\
            = _number.get_text(strip=True).replace('最新号', '') if _number is not None else ''
        _release_date = tag_salesinfo1.find(string=re.compile('発売日'))
        _price = tag_salesinfo1.find(string=re.compile('価格'))
        magazine_data.release_date = __extract_date(_date=_release_date)
        magazine_data.price = __extract_price(_price=_price)

        for tag_b in tag_salesinfo1.find_all('b', string='【特集】'):
            magazine_data.top_outlines.append(
                tag_b.parent.get_text(strip=True)
            )

        _store_link = tag_salesinfo1.find('a', href=re.compile('amazon'))
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='Amazon',
                    url=_store_link.get('href')
                )
            )
        _store_link = tag_salesinfo1.find('a', href=re.compile('books.rakuten'))
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='Rakutenブックス',
                    url=_store_link.get('href')
                )
            )
    return magazine_data

def __scrape_nikkei_linux():
    _url = 'https://info.nikkeibp.co.jp/media/LIN/'
    magazine_data = ItMagazineData(name='日経Linux', url=_url)

    soup = __get_soup(_url)
    tag_salesinfo1 = soup.find('div', class_='articleBody')
    if tag_salesinfo1 is not None:
        tag_salesinfo1 = tag_salesinfo1.find('div', class_='cover-txt')
    if tag_salesinfo1 is not None:
        _number = tag_salesinfo1.find('p', class_='Title')
        magazine_data.number\
            = _number.get_text(strip=True).replace('最新号', '') if _number is not None else ''
        _release_date = tag_salesinfo1.find(string=re.compile('発売日'))
        _price = tag_salesinfo1.find(string=re.compile('価格'))
        magazine_data.release_date = __extract_date(_date=_release_date)
        magazine_data.price = __extract_price(_price=_price)

        for tag_b in tag_salesinfo1.find_all('b', string=re.compile('【特集')):
            magazine_data.top_outlines.append(
                tag_b.parent.get_text(strip=True)
            )

        _store_link = tag_salesinfo1.find('a', href=re.compile('amazon'))
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='Amazon',
                    url=_store_link.get('href')
                )
            )
        _store_link = tag_salesinfo1.find('a', href=re.compile('books.rakuten'))
        if _store_link is not None:
            magazine_data.store_links.append(
                ItMagazineStoreLink(
                    name='Rakutenブックス',
                    url=_store_link.get('href')
                )
            )
    return magazine_data

def scrape_magazine(magazine_type: ItMagazineType) -> ItMagazineData:
    '''
    scrape magazine
    '''
    print(f'{magazine_type.name} scraping ...', end='')
    _magazine: ItMagazineData = None
    if magazine_type == ItMagazineType.SOFTWARE_DESIGN:
        _magazine = __scrape_software_design()
    elif magazine_type == ItMagazineType.WEB_DB_PRESS:
        _magazine = __scrape_web_db_press()
    elif magazine_type == ItMagazineType.INTERFACE:
        _magazine = __scrape_interface()
    elif magazine_type == ItMagazineType.TRANGISTOR_GIJUTSU:
        _magazine = __scrape_trangistor_gijutsu()
    elif magazine_type == ItMagazineType.NIKKEI_SOFTWARE:
        _magazine = __scrape_nikkei_software()
    elif magazine_type == ItMagazineType.NIKKEI_LINUX:
        _magazine = __scrape_nikkei_linux()
    print('done')
    return _magazine

def scrape_magazines() -> List[ItMagazineData]:
    '''
    scrape magazines
    '''
    _magazines: List[ItMagazineData] = []
    for magazine_type in ItMagazineType:
        _magazines.append(scrape_magazine(magazine_type=magazine_type))
    return _magazines

if __name__ == '__main__':
    for magazine in scrape_magazines():
        print(magazine.get_json())
