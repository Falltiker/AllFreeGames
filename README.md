# Free Games Parser

> ⚠️ Внимание: данный проект использует неофициальные методы получения данных. Он предназначен только для ознакомительных и образовательных целей.

Если хотите что-то спросить или дополнить проект — пишите: [Telegram](https://t.me/Falltiker)

Скрипт для получения бесплатных игр из **Epic Games Store** и **Steam**.

Проект собирает информацию о бесплатных играх, формирует отчёты в форматах **JSON** и **Markdown**, и сохраняет их в файлы.

---

## Файл FreeGames.md

Пример содержимого `epic_games.md`:

![Содержимое FreeGames.md](img/Markdown.png)

---

## 🔧 Установка

1. Клонируй репозиторий или скачай архив с кодом.
2. Установи зависимости:

```bash
pip install -r requirements.txt
```

Все зависимости перечислены в `requirements.txt`, вот основные:

- `requests`
- `beautifulsoup4`
- `lxml`
- `fake-useragent`


---

## 🚀 Использование

```bash
python main.py
```

После запуска ты получишь:

- `FreeGames.json` — файл со структурированной информацией о всех играх.
- `epic_games.md` — красиво отформатированный Markdown-отчёт.
- `logging.log` — лог-файл выполнения скрипта.

---

## 🗂 Структура проекта

```
.
├── main.py
├── parsers/
│   ├── __init__.py
│   ├── epicgames.py
│   └── steam.py
├── requirements.txt
├── FreeGames.json
├── epic_games.md
└── logging.log
```

---

## 📜 Лицензия

Этот проект лицензирован по лицензии [MIT](LICENSE). Подробности смотри в файле LICENSE.
