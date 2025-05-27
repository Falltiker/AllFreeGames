import requests
import json
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import logging



def get_games_steam():
    headers = {
        'Referer': 'https://store.steampowered.com/search/?force_infinite=1&maxprice=free&specials=1&ndl=1',
        'User-Agent': UserAgent().random,
        'Accept': '*/*',
    }

    # Отправляем запрос и получаем в ответ безплатные длс и игры
    response = requests.get('https://store.steampowered.com/search/results?force_infinite=1&maxprice=free&specials=1&ndl=1&snr=1_7_7_230_7', headers=headers)
    soup = BS(response.text, "lxml")
    logging.info("Отправка запроса на сервер Steam...")

    all_games = soup.find("div", id="search_resultsRows")
    all_games = all_games.find_all("a")
    logging.info(f"Получено {len(all_games)} игр из API.")
    games_list = list()
    for game in all_games:
        try:
            title = game.find("span", class_="title").text
            logging.info(f"Обработка игры: {title}")
            # Проверяем, что игра бесплатная
            discounted_price_tag = game.find("div", class_="discount_final_price")
            discounted_price = discounted_price_tag.text.strip() if discounted_price_tag else 0
            currency_symbol = discounted_price[-1] # Сохраняем символ валюты
            discounted_price = str(discounted_price).replace(",", ".")[:-1]  # Убираем знак валюты, меняем запятую на точку для преобразования в float
            discounted_price = float(discounted_price)
            logging.debug(f"Цена игры {title}: {discounted_price}{currency_symbol}")
            # Проверяем, что цена нулевая. Не знаю почему, но иногда игра может быть не со 100% скидкой, хотя фильтр я поставил нормально.
            if discounted_price != 0:
                logging.debug(f"Игра {title} не бесплатна, цена: {discounted_price}")
                continue

            url = game.get("href")
            logging.debug(f"URL игры {title}: {url}")
            image = game.find("div", class_="search_capsule").find("img").get("src")
            logging.debug(f"Изображение игры {title}: {image}")
            original_price = game.find("div", class_="discount_original_price")
            logging.debug(f"Цена без скидки {title}: {original_price.text.strip() if original_price else 'Нет оригинальной цены'}")

            res = requests.get(url)
            soup = BS(res.text, "lxml")
            logging.debug(f"Получен HTML-код страницы игры {title}.")

            desc_tag = soup.find("div", class_="game_description_snippet")
            description = desc_tag.text.strip() if desc_tag else "Описание не найдено"
            logging.debug(f"Описание игры {title}: {description}")

            mini_div_info = soup.find("div", class_="glance_ctn_responsive_left")

            reviews = mini_div_info.find_all("div", class_="user_reviews_summary_row")
            recent_reviews = reviews[0]["data-tooltip-html"]
            logging.debug(f"Недавние отзывы для игры {title}: {recent_reviews}")

            all_reviews = reviews[-1]["data-tooltip-html"]
            logging.debug(f"Все отзывы для игры {title}: {all_reviews}")

            release_date_tag = mini_div_info.find("div", class_="date")
            release_date = release_date_tag.text.strip() if release_date_tag else "Дата выпуска не указана"
            logging.debug(f"Дата выпуска игры {title}: {release_date}")

            developer_url = mini_div_info.find("div", id="developers_list").find("a")["href"]
            developer_name_tag = mini_div_info.find("div", id="developers_list").find("a")
            developer_name = developer_name_tag.text.strip() if developer_name_tag else "Разработчик не указан"
            developer = {
                "name": developer_name,
                "url": developer_url
            }
            logging.debug(f"Разработчик игры {title}: {developer_name} ({developer_url})")

            publisher_tag = mini_div_info.find_all("div", class_="dev_row")[-1]

            if publisher_tag:
                publisher_link = publisher_tag.find("a")
                publisher_name = publisher_link.text.strip() if publisher_link else "Издатель не указан"
                publisher_url = publisher_link["href"] if publisher_link and publisher_link.has_attr("href") else "Издатель не указан"
            else:
                publisher_name = "Издатель не указан"
                publisher_url = "Издатель не указан"

            publisher = {
                "name": publisher_name,
                "url": publisher_url
            }

            dlc = soup.find("div", class_="game_area_bubble game_area_dlc_bubble")
            if dlc:
                dlc_url = dlc.find("a")["href"]
                dlc_name_tag = dlc.find("a")
                dlc_name = dlc_name_tag.text.strip()
                dlc = {
                    "name": dlc_name,
                    "url": dlc_url
                }
            else:
                dlc = None
            logging.debug(f"DLC - Продукт {title} является дополнением (DLC): {dlc['name']} ({dlc['url']})" if dlc else "DLC не найдено")

            games_list.append({
                "title": title,
                "url": url,
                "image": image,
                "description": description,
                "discounted_price": discounted_price,
                "currency_symbol": currency_symbol,
                "original_price": original_price.text.strip() if original_price else "Нет оригинальной цены",
                "developer": developer,
                "publisher": publisher,
                "release_date": release_date,
                "recent_reviews": recent_reviews,
                "all_reviews": all_reviews,
                "dlc": dlc
            })
            logging.info(f"Игра {title} успешно обработана.")

        except Exception as e:
            logging.error(f"Ошибка при обработке игры: {e}")

        return games_list


if __name__ == "__main__":
    get_games_steam()