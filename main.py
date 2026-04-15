import logging

from data import DataHandler
from errors import InvalidPageFormatError
from scrapper import WebScrapper


def main():
    url = "http://www.ppgee.eng.ufba.br/default.php"
    web_scrapper = WebScrapper(url)
    try:
        news = web_scrapper.get_news()
        handler = DataHandler()
        handler.save_data(news)
    except InvalidPageFormatError as err:
        logging.error(err)


if __name__ == "__main__":
    main()
