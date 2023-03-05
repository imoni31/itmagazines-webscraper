# itmagazines-webscraper

This libraly is web scraper for web pages of IT-Magazine.

## Support magazine list

* 技術評論社
    * Software Design
    * WEB+DB PRESS
* CQ出版
    * Interface
    * トランジスタ技術
* 日経
    * 日経ソフトウエア
    * 日経Linux

## Installaction

```console
$ python -m pip install itmagazines-webscraper
```

## Usage

### Specify a magazine and execute
```python
from pprint import pprint
from itmagazines_webscraper import ItMagazineType, scrape_magazine

magazine = scrape_magazine(ItMagazineType.SOFTWARE_DESIGN)
pprint(magazine.get_dict())
print(magazine.get_json())
```

### Execute all
```python
from pprint import pprint
from itmagazines_webscraper import scrape_magazines

for magazine in scrape_magazines():
    pprint(magazine.get_dict())
    print(magazine.get_json())
```
