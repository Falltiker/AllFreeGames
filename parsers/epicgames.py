import requests
import json
import logging
from datetime import datetime

def get_free_epic_games(locale="ru", country="UA"):
    logging.info("Запрашиваем список бесплатных игр из Epic Games Store.")
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    params = {
        "locale": locale,
        "country": country,
        "allowCountries": country
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.info("Данные успешно получены от API.")
    except requests.RequestException as e:
        logging.exception("Ошибка при получении данных из API Epic Games.")
        raise

    with open("1.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        logging.debug("Данные API сохранены в 1.json для отладки.")

    games = data['data']['Catalog']['searchStore']['elements']
    free_games = []

    for i, game in enumerate(games, start=1):
        title = game.get("title", "Без названия")
        logging.debug(f"[{i}] Проверяется игра: {title}")

        if "Mystery Game" in title or "LISA: Definitive Edition" in title:
            logging.debug(f"[{i}] Пропущена игра Mystery Game.")
            continue

        image = [img.get("url") for img in game.get("keyImages", [])]
        if not image:
            logging.warning(f"[{i}] У игры '{title}' нет изображений.")


        slug = game.get("productSlug")
        logging.debug(f"[{i}] У игры '{title}' productSlug = {slug}.")

        categories = game.get("categories", [])
        category = categories[0]["path"] if categories else "unknown"

        if slug:
            url = f"https://store.epicgames.com/ru/{'bundles' if category == 'bundles' else 'p'}/{slug}"
        else:
            logging.warning(f"[{i}] У игры '{title}' отсутствует productSlug.")
            continue
            url = None

        description = game.get("description", "")


        # Числа в которые игра будет бесплатная
        # Пока что, нормально не работает

        # start = game.get("effectiveDate")
        # end = game.get("expiryDate")

        # if not start or not end:
        #     logging.info(f"[{i}] Пропущена игра '{title}' — отсутствует effectiveDate или expiryDate.")
        #     continue

        # try:
        #     start_fmt = datetime.fromisoformat(start.replace("Z", "+00:00")).strftime("%d.%m.%Y")
        #     end_fmt = datetime.fromisoformat(end.replace("Z", "+00:00")).strftime("%d.%m.%Y")
        # except Exception as e:
        #     logging.warning(f"[{i}] Ошибка при парсинге дат у '{title}': {e}")
        #     start_fmt = end_fmt = "?"

        free_games.append({
            "title": title,
            "image": image,
            "description": description,
            "url": url
            # "start_date": start_fmt,
            # "end_date": end_fmt
        })
        logging.info(f"[{i}] Игра '{title}' добавлена в список")

    logging.info(f"Обработано {len(free_games)} бесплатных игр.")

    # Markdown
    md = "## 🎮 Бесплатные игры из Epic Games Store\n\n"
    md += "| Игра | Даты раздачи | Ссылка |\n|------|----------------|--------|\n"
    for g in free_games:
        md += f"| {g['title']} | [картинка]({g['image'][0] if g['image'] else 'нет'}) | [Ссылка]({g['url']}) |\n"

    return free_games, md
