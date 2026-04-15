from datetime import datetime
from typing import List
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup
from requests import get

from errors import InvalidPageFormatError
from schemas import News


class WebScrapper:
    def __init__(self, url: str):
        self.url = url

    def _read_page_content(self) -> str:
        result = get(self.url)
        return result.text

    def get_news(self) -> List[News]:
        content = self._read_page_content()
        soup = BeautifulSoup(content, "html.parser")
        news_div = soup.find("div", id="col_dir")
        if not news_div:
            raise InvalidPageFormatError("Invalid page format: 'col_dir' div not found")

        h4 = news_div.find("h4")
        if not h4:
            raise InvalidPageFormatError(
                "Invalid page format: 'h4' element not found within 'col_dir' div"
            )

        h4_content: str = h4.get_text()
        if (
            "notícias" not in h4_content.lower()
            and "noticies" not in h4_content.lower()
        ):
            raise InvalidPageFormatError(
                "Invalid page format: 'h4' element does not contain expected news title"
            )

        paragraphs = news_div.find_all("p")

        if not paragraphs or len(paragraphs) == 0:
            raise InvalidPageFormatError(
                "Invalid page format: No news paragraphs found within 'col_dir' div"
            )

        news = []
        for p in paragraphs:
            a = p.find("a", class_="noticia")
            if not a:
                continue
            news_date_str = p.contents[0].get_text(strip=True)
            news_date = datetime.strptime(news_date_str, "%d/%m/%Y")
            news_title = a.get_text(strip=True)
            href = str(a.get("href"))
            news_url = urljoin(self.url, href)
            parsed_href = urlparse(href)
            query = parse_qs(parsed_href.query)
            news_id = query.get("id", [None])[0]

            if not news_date or not news_title or not news_url or not news_id:
                raise InvalidPageFormatError(
                    "Invalid page format: Incomplete news information"
                )

            news_id_int = int(news_id)
            news.append(
                News(title=news_title, url=news_url, date=news_date, id=news_id_int)
            )

        return news


__all__ = ["WebScrapper"]
