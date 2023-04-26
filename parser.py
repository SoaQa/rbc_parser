import requests
from bs4 import BeautifulSoup

from messages.decorators import mute_exceptions

SITE_URL = "https://www.rbc.ru/"


@mute_exceptions
def get_rbc_news():
    rows = [f"Новости с сайта {SITE_URL}"]
    row = "{title}: {url}"
    pro_rows = []

    res = requests.get(SITE_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    main_news = soup.find(attrs={"data-vr-zone": "Главная новость"})
    rows.append(
        row.format(
            title=main_news.find(name='span', attrs={"class": "main__big__title"}).text,
            url=main_news.find(name='a').attrs["href"]
        )
    )

    main_list = soup.find(name="div", attrs={"class": "main__list"})
    main_inners = main_list.find_all(name="div", attrs={"class": "main__inner"})
    for i in main_inners:
        for j in i.find_all(attrs={"class": "main__feed"}):

            href = j.find(name='a').attrs["href"]
            if "pro.rbc.ru" in href:
                pro_rows.append(
                    row.format(
                        title=j.find(name='span', attrs={"class": "main__feed__title"}).text,
                        url=href
                    )
                )
                continue

            rows.append(
                row.format(
                    title=j.find(name='span', attrs={"class": "main__feed__title"}).text,
                    url=href
                )
            )
    rows.append("Далее новости rbc.pro, нужна подписка...")
    rows.extend(pro_rows)
    return rows
