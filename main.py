import logging
import json
from parsers import steam, epicgames


"""Скрипт для получения бесплатных игр из Epic Games Store и Steam.
Этот скрипт собирает информацию о бесплатных играх из Epic Games Store и Steam,
формирует отчёт в формате JSON и Markdown, а также сохраняет результаты в файлы.
Он использует библиотеки requests и BeautifulSoup для парсинга HTML-страниц."""

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logging.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("Скрипт запущен.")

try:
    games_epic = epicgames.get_games_epicgames()
    logging.info(f"В EpicGames сейчас бесплатно {len(games_epic["current"])} игор и {len(games_epic["upcoming"])} в скором будущем будут бесплатны.")
    
    games_steam = steam.get_games_steam()
    if not games_steam:
        logging.info("В Steam нет бесплатных игр. Завершаем работу скрипта.")
    else:
        logging.info(f"В Steam сейчас бесплатно {len(games_steam)} игор.")

    # Сохраняем результаты в JSON-файл
    games_all = {
        "epic_games": games_epic,
        "steam_games": games_steam
    }
    with open("FreeGames.json", "w", encoding="utf-8") as f:
        json.dump(games_all, f, ensure_ascii=False, indent=4)
        logging.info("Файл FreeGames.json успешно сохранён.")

    # Формируем Markdown-отчёт
    games_current = games_epic["current"]
    games_upcoming = games_epic["upcoming"]
    md = "## Epic Games Store\n\n"
    md += "### Сейчас бесплатно:\n\n"
    md += "| Игра | Даты раздачи | Ссылка |\n|------|----------------|--------|\n"
    for g in games_current:
        md += f"| {g['title']} | {g['start_date']} — {g['end_date']} | [Ссылка]({g['url']}) |\n"

    md += "\n### Будущие раздачи:\n\n"
    for g in games_upcoming:
        md += f"| {g['title']} | {g['start_date']} — {g['end_date']} | [Ссылка]({g['url']}) |\n"

    if games_steam:
        md += "\n\n----------------------------------------------\n\n"
        md += "\n\n## Steam\n\n"
        md += "| Игра | Ссылка |\n|------|--------|\n"
        for g in games_steam:
            md += f"| {g['title']} | [Ссылка]({g['url']}) |\n"

    # Сохраняем Markdown-отчёт в файл
    with open("FreeGames.md", "w", encoding="utf-8") as mf:
        mf.write(md)
        logging.info("Файл epic_games.md успешно сохранён.")


except Exception as e:
    logging.exception(f"Произошла ошибка при выполнении скрипта - {e}")

logging.info("Скрипт завершён.")
