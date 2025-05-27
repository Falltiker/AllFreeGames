import requests
import logging
from datetime import datetime

def get_games_epicgames(locale="ru", country="UA"):
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    params = {
        "locale": locale,
        "country": country,
        "allowCountries": country
    }

    logging.info("Отправка запроса на сервер Epic Games...")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.info("Данные успешно получены.")
    except Exception as e:
        logging.error(f"Ошибка при получении данных от Epic Games: {e}")
        return {}, ""

    games = data['data']['Catalog']['searchStore']['elements']
    logging.info(f"Получено {len(games)} игр из API.")

    free_games = {
        "current": [],
        "upcoming": []
    }

    current_date = datetime.now().date()

    for i, game in enumerate(games, start=1):
        title = game.get("title", "Без названия")
        logging.debug(f"[{i}] Проверка игры: {title}")

        if "Mystery Game" in title:
            logging.info(f"[{i}] Пропущена игра '{title}' (Mystery Game).")
            continue

        image = [img.get("url") for img in game.get("keyImages", [])]
        if not image:
            logging.warning(f"[{i}] У игры '{title}' нет изображений.")

        slug = game.get("productSlug")
        if not slug:
            logging.warning(f"[{i}] У игры '{title}' отсутствует productSlug.")
        category = game["categories"][0]["path"] if game.get("categories") else "unknown"

        if slug:
            url = f"https://store.epicgames.com/ru/{'bundles' if category == 'bundles' else 'p'}/{slug}"
        else:
            url = None

        description = game.get("description", "")
        promotions = game.get("promotions", {})
        if not promotions:
            logging.info(f"[{i}] У игры '{title}' отсутствуют акции.")
            continue

        promotional_offers = promotions.get('promotionalOffers', [])
        if not promotional_offers:
            logging.info(f"[{i}] У игры '{title}' нет активных раздач.")
            continue

        offers = promotional_offers[0].get('promotionalOffers', [])
        for promo in offers:
            if promo.get("discountSetting", {}).get("discountPercentage") == 0:
                start = promo.get("startDate")
                end = promo.get("endDate")
                try:
                    start_date = datetime.fromisoformat(start.replace("Z", "+00:00")).date()
                    end_date = datetime.fromisoformat(end.replace("Z", "+00:00")).date()
                except Exception as e:
                    logging.warning(f"[{i}] Ошибка парсинга дат у игры '{title}': {e}")
                    start_date = end_date = None

                if start_date and end_date and start_date <= current_date <= end_date:
                    logging.info(f"[{i}] Игра '{title}' сейчас бесплатна.")
                    free_games["current"].append({
                        "title": title,
                        "description": description,
                        "url": url,
                        "start_date": start_date.strftime("%d.%m.%Y"),
                        "end_date": end_date.strftime("%d.%m.%Y"),
                    })
                elif start_date and start_date > current_date:
                    logging.info(f"[{i}] Игра '{title}' будет раздаваться в будущем.")
                    free_games["upcoming"].append({
                        "title": title,
                        "description": description,
                        "url": url,
                        "start_date": start_date.strftime("%d.%m.%Y"),
                        "end_date": end_date.strftime("%d.%m.%Y"),
                    })

    return free_games


# Тестовый запуск
if __name__ == "__main__":
    get_games_epicgames()
