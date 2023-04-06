import os
import xml.etree.ElementTree as ET
from urllib.request import urlopen

def save_curs(curs):
    with open('last_curs.txt', 'w') as f:
        f.write(f'{curs}')

def get_dollar_rate():
    """ Получить курс рубля к доллару от ЦБ на сегодня. """
    try:
        with urlopen("https://www.cbr.ru/scripts/XML_daily.asp", timeout=5) as r:
            curs = (ET.parse(r).findtext('.//Valute[@ID="R01235"]/Value'))
            save_curs(curs)
            return float(curs.replace(',', '.'))
    except Exception as e:
        print(f'ERROR {e}')
        with open('last_curs.txt', 'r') as f:
            curs = next(f).strip()
            return float(curs.replace(',', '.'))

def slice_list(result_list):
    result = result_list[1:]
    return result



if __name__ == "__main__":
    curs = get_dollar_rate()
    print(type(curs))
    print(f'1 доллар = {curs} руб.')