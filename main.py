from parsers.epicgames import get_free_epic_games
import json


games, markdown = get_free_epic_games()
print(markdown)

# сохранить
with open("epic_games.json", "w", encoding="utf-8") as jf:
    json.dump(games, jf, ensure_ascii=False, indent=2)

with open("epic_games.md", "w", encoding="utf-8") as mf:
    mf.write(markdown)
