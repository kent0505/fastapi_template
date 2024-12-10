from fastapi  import APIRouter
from bs4      import BeautifulSoup
from datetime import datetime, timedelta

import requests

router = APIRouter()

@router.get("/")
async def get_fixtures():
    date = datetime.now() - timedelta(days=1)
    yesterday: str = date.strftime("%-d-%B-%Y")

    url = f"https://www.skysports.com/football/fixtures-results/{yesterday}"
    headers: dict = {"User-Agent": "Mozilla/5.0"}
    response = await requests.get(url, headers)

    soup = BeautifulSoup(response.text, "lxml")

    data = soup.find_all("div", class_="fixres__item")

    fixtures = []

    for i in data:
        try:
            a = i.find("a", class_="matches__item matches__link")
            scores = i.find_all("span", class_="matches__teamscores-side")
            titles = i.find_all("span", class_="swap-text--bp30")
            if len(scores) and len(titles) == 2:
                score1 = scores[0].text.strip()
                score2 = scores[1].text.strip()
                title1 = titles[0].get("title")
                title2 = titles[1].get("title")
                fixtures.append({
                    {
                            "home": {
                                "title": title1,
                                "score": score1,
                            },
                            "away": {
                                "title": title2,
                                "score": score2,
                            },
                            
                        }
                })
                # print(f"{title1} {score1}:{score2} {title2}")
        except Exception as e:
            print(e)

        
    return {
                    "fixtures": [
                        fixture
                    ]
                    for fixture in fixtures
                }

    # for div in data:
    #     print(div.text.strip())

    #     links = div.find_all('a')
    #     for link in links:
    #         print(link.get('href'))