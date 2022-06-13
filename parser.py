from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class News:
    date: datetime
    title: str
    content: str
    tags: list[str]


class NewsPageParser(ABC):
    @abstractmethod
    def parse_page(self, url: str) -> News:
        pass


class NewsSite(ABC):
    def __init__(self, parser: NewsPageParser) -> None:
        self._parser = parser

    def provide_today_news_page(self) -> list[str]:
        return self.provide_news_pages_for(date=datetime.now())

    def provide_today_news(self) -> list[News]:
        return [self._parser.parse_page(url=url_) for url_ in self.provide_today_news_page()]

    @abstractmethod
    def provide_news_pages_for(self, date: datetime) -> list[str]:
        pass

    def provide_news_for(self, date: datetime) -> list[News]:
        return [self._parser.parse_page(url=url_) for url_ in self.provide_news_pages_for(date=date)]

    @abstractmethod
    def provide_last_news_page(self) -> str:
        pass

    def provide_last_news(self) -> News:
        return self._parser.parse_page(url=self.provide_last_news_page())
