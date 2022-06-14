import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import requests

from parser import NewsSite, NewsPageParser, News


class RiaNewsPageParser(NewsPageParser):
    def parse_page(self, url: str) -> News:
        pass


class RiaNewsSite(NewsSite):
    def __init__(self) -> None:
        super().__init__(parser=RiaNewsPageParser(), site_name='ria.ru')
        self._required_date: datetime = datetime.now()
        self._is_required_date = True

    def provide_news_pages_for(self, date: datetime) -> list[str]:
        self._required_date = date
        date_in_url = date.strftime('%Y%m%d')
        url_ = f"https://ria.ru/{date_in_url}"

        urls = []
        while self._is_required_date:
            soup_ = self._provide_soup(url=url_)
            urls.extend(self._provide_urls(soup=soup_))
            url_ = self._provide_next_url(soup=soup_)
            if url_ == 'https://ria.ru':
                break
        return urls

    def provide_last_news_page(self) -> str:
        url_ = 'https://ria.ru/lenta/'
        soup_ = self._provide_soup(url=url_)
        return self._provide_urls(soup=soup_)[0]

    @staticmethod
    def _provide_soup(url: str) -> BeautifulSoup:
        request = requests.get(url=url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/74.0.3729.169 Safari/537.36'})
        return BeautifulSoup(request.text, 'lxml')

    def _provide_urls(self, soup: BeautifulSoup) -> list[str]:
        urls = []
        for item in soup.find_all(name='div', class_='list-item'):
            text_with_date_ = item.find(name='div', class_='list-item__date').text
            self._update_date(text_with_date=text_with_date_)
            if not self._is_required_date:
                break
            urls.append(item.find(name='a', class_='list-item__title color-font-hover-only')['href'])
        return urls

    def _update_date(self, text_with_date: str) -> None:
        if self._required_date.date() == datetime.now().date():
            self._is_required_date = True if re.fullmatch(r'\d\d:\d\d', text_with_date) else False
        elif self._required_date.date() == (datetime.now() - timedelta(days=1)).date():
            self._is_required_date = True if re.fullmatch(r'Вчера, \d\d:\d\d', text_with_date) else False
        else:
            self._is_required_date = True if int(text_with_date.split()[0]) == self._required_date.day else False

    @staticmethod
    def _provide_next_url(soup: BeautifulSoup) -> str:
        if soup.find(name='div', class_='list-more'):       # Human-readble page
            return f"https://ria.ru{soup.find(name='div', class_='list-more')['data-url']}"
        else:   # Loading the pagination content
            return f"https://ria.ru{soup.find(name='div', class_='list-items-loaded')['data-next-url']}"
