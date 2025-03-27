import requests
import json
from datetime import datetime

def get_free_epic_games(locale="ru", country="UA"):
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    params = {
        "locale": locale,
        "country": country,
        "allowCountries": country
    }
    response = requests.get(url, params=params)
    data = response.json()

    # with open("1.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)

    games = data['data']['Catalog']['searchStore']['elements']
    free_games = []

    for game in games:
        title = game.get("title", "Без названия")
        if "Mystery Game" in title:
            continue

        image = []
        image_temp = game.get("keyImages")
        for img in image_temp:
            image.append(img.get("url"))

        slug = game.get("productSlug")
        if slug:
            category = game["categories"][0]["path"]
            if category == "bundles":
                url = f"https://store.epicgames.com/ru/bundles/{slug}"
            else:
                url = f"https://store.epicgames.com/ru/p/{slug}"

        else:
            url = None  # Если productSlug отсутствует
        
        description = game.get("description", "")
        promotions = game.get("promotions", {})
        offer = None

        # Берем либо текущие, либо будущие раздачи
        if game.get("effectiveDate"):
            start = game.get("effectiveDate")
        else:
            continue
        if game.get("expiryDate"):
            end = game.get("expiryDate")
        else:
            continue

        try:
            start = datetime.fromisoformat(start.replace("Z", "+00:00")).strftime("%d.%m.%Y")
            end = datetime.fromisoformat(end.replace("Z", "+00:00")).strftime("%d.%m.%Y")
        except:
            start = end = "?"

        free_games.append({
            "title": title,
            "image": image,
            "description": description,
            "url": url,
            "start_date": start,
            "end_date": end
        })

    # Markdown
    md = "## 🎮 Бесплатные игры из Epic Games Store\n\n"
    md += "| Игра | Даты раздачи | Ссылка |\n|------|----------------|--------|\n"
    for g in free_games:
        md += f"| {g['title']} | [картинка]({g['image'][0]}) | [Ссылка]({g['url']}) |\n"

    return free_games, md
