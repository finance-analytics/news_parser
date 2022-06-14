import os.path
import sys
from datetime import datetime, timedelta
from time import sleep

from parser import NewsSite
from ria import RiaNewsSite

DIR_WITH_URLS = 'results'


def launch_spider(site: NewsSite, start_date: str, show_progress: bool | None = True) -> None:
    date_ = datetime.strptime(start_date, '%d.%m.%Y') - timedelta(days=1)
    day_delta = (datetime.now() - date_).days
    problems = 0

    for i in range(day_delta):
        date_ += timedelta(days=1)

        if show_progress:
            sys.stdout.write(f"\rProgress ({site.site_name}): {i / day_delta * 100 :.3f}%\tProblems: {problems}\t"
                             f"Date: {date_.strftime('%d.%m.%Y')}")
            sys.stdout.flush()

        if os.path.exists(_provide_path_to_file(site_name=site.site_name, date=date_)):
            continue

        try:
            urls_ = site.provide_news_pages_for(date=date_)
            _save_urls(site_name=site.site_name, date=date_, urls=urls_)
            sleep(0.7)
        except:
            problems += 1
            continue


def _provide_path_to_file(site_name: str, date: datetime) -> str:
    return f"{DIR_WITH_URLS}/{site_name}/{date.strftime('%Y_%m_%d')}"


def _save_urls(site_name: str, date: datetime, urls: list[str]) -> None:
    if not urls:
        return

    if not os.path.exists(DIR_WITH_URLS):
        os.mkdir(DIR_WITH_URLS)
    if not os.path.exists(f"{DIR_WITH_URLS}/{site_name}"):
        os.mkdir(f"{DIR_WITH_URLS}/{site_name}")
    with open(_provide_path_to_file(site_name=site_name, date=date), 'w') as file:
        file.write('\n'.join(urls))


def _main() -> None:
    sites = (
        (RiaNewsSite(), '16.10.2001'),
    )

    for site_, start_date_ in sites:
        launch_spider(site=site_, start_date=start_date_)


if __name__ == '__main__':
    _main()
