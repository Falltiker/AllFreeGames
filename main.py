import logging
import json
# from parsers.epicgames import get_free_epic_games
from epicgamesV2 import get_free_epic_games

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("Скрипт запущен.")

try:
    games, markdown = get_free_epic_games()
    logging.info(f"Получено {len(games)} бесплатных игр.")

    with open("epic_games.json", "w", encoding="utf-8") as jf:
        json.dump(games, jf, ensure_ascii=False, indent=4)
        logging.info("Файл epic_games.json успешно сохранён.")

    with open("epic_games.md", "w", encoding="utf-8") as mf:
        mf.write(markdown)
        logging.info("Файл epic_games.md успешно сохранён.")

except Exception as e:
    logging.exception(f"Произошла ошибка при выполнении скрипта - {e}")

logging.info("Скрипт завершён.")
