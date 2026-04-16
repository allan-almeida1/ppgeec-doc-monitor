import logging

from data import DataHandler
from errors import InvalidPageFormatError
from mail import MailSender
from scrapper import WebScrapper


def main():
    url = "http://www.ppgee.eng.ufba.br/default.php"
    web_scrapper = WebScrapper(url)
    try:
        news = web_scrapper.get_news()
        handler = DataHandler()
        saved_news = handler.get_data()

        # Check for fresh news
        old_ids = {n.id for n in saved_news}
        new_items = [n for n in news if n.id not in old_ids]

        if new_items:
            news_list = ""
            for item in new_items:
                news_list += (
                    f"<li><a href='{item.url}' target='_blank'>{item.title}</a></li>"
                )
            mail_sender = MailSender()
            plural = "s" if len(new_items) > 1 else ""
            subject = f"🆕 PPGEEC - Nova{plural} Notícia{plural} Publicadas"
            body = f"""
            <p>Nova{plural} notícia{plural} no PPGEEC</p>
            
            <ul>{news_list}</ul>
            """

            mail_sender.send_email(subject, body)

        handler.save_data(news)
    except InvalidPageFormatError as err:
        logging.error(err)


if __name__ == "__main__":
    main()
