# itmagazines-webscraper

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

```python
from itmagazines_webscraper import ItMagazineType, scrape_magazine

magazine = scrape_magazine(ItMagazineType.SOFTWARE_DESIGN)
print(magazine.get_json())
```

```python
from itmagazines_webscraper import scrape_magazines

for magazine in scrape_magazines():
    print(magazine.get_json())
```
