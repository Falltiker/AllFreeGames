# Получаем список всех игор и длс со скидкой в 100% со стима
# Отправляет get запрос, что бы получить список
# Собираю информацию о контенте только названия, цены и ссылки


import requests
import json
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent



def main():
    headers = {
        'Referer': 'https://store.steampowered.com/search/?force_infinite=1&maxprice=free&specials=1&ndl=1',
        'User-Agent': UserAgent().random,
        'Accept': '*/*',
    }

    params = {
        'force_infinite': '1',
        'maxprice': 'free',
        'specials': '1',
        'ndl': '1',
        'snr': '1_7_7_2300_7',
    }

    # with open("index.html", "r", encoding="utf-8") as f:
    #     res = f.read()
    # res = BS(res, "lxml")

    # Отправляем запрос и получаем в ответ безплатные длс и игры
    response = requests.get('https://store.steampowered.com/search/results', params=params, headers=headers)
    soup = BS(response.text, "lxml")
    
    # with open("index.html", "w", encoding="utf-8") as f:
    #     f.write(str(soup))

    # Каждый блок с игрой <a>, делаем список для удобства
    res = soup.find_all("a")

    # Получаем информицаю игор со списка
    games_dict = dict()
    for i in res:
        name = i.find("span").text
        url =  i["href"]
        # img =  i.find("img")["src"]
        # date = i.find("div", class_="col search_released responsive_secondrow").text.strip()
        price =i.find("div", class_="discount_original_price")
        # Класы меняется, заметил сходность что discount_final_price это длс до контента
        if price:
            price = price.text.strip()
            dlc = None # Заметил сходность, по класу блока цены можно опредилить доп контент
        else:
            price = i.find("div", class_="discount_final_price").text.strip()
            dlc = True # Заметил сходность, по класу блока цены можно опредилить доп контент

        platforms_temp = i.find("div", class_="col search_name ellipsis").find_all("span")[1:]
        # Получем в удобном виде платформы поддерживаюшие игру
        platforms = list()
        for platform in platforms_temp:
            platforms.append(str(platform["class"][-1]))


        # Если нашли бесплатное длс, смотрим какая игра нужна для него и информацию о ней
        if dlc:
            # Заходим на страницу длс
            res = requests.get(url, headers=headers, params=params)
            soup = BS(res.text, "lxml")

            # Получаем и переходим ссылку на контент к которому длс 
            dlc_url = soup.find("div", class_="game_area_bubble game_area_dlc_bubble").find("a")["href"]

            res = requests.get(dlc_url, params=params, headers=headers)
            soup = BS(res.text, "lxml")

            # Получаем информацию о нашей игре
            dlc_name = soup.find("div", id="appHubAppName").text.strip()
            # dlc_img = soup.find("div", id="gameHeaderImageCtn").find("img")["src"]
            dlc_price_free = soup.find("a", class_="btn_green_steamui btn_medium").text.strip()
            if str(dlc_price_free) in "Играть":
                dlc_price = "Free"
                dlc = {
                    dlc_name: {
                        # "img": dlc_img,
                        "price": dlc_price
                    }
                }
            else:
                dlc_price_temp = soup.find("div", class_="discount_block game_purchase_discount")
                dlc_price_original = dlc_price_temp.find("div", "discount_original_price").text.strip()
                dlc_price_final = dlc_price_temp.find("div", "discount_final_price").text.strip()

                dlc = {
                    dlc_name: {
                        # "img": dlc_img,
                        "price_original": dlc_price_original,
                        "price_final": dlc_price_final
                    }
                }

        # Упаковываем в словарь и сохраняем в json файл
        games_dict[name] = {
            "url": url,
            # "img": img,
            # "date": date,
            "price": price,
            "platform": platforms,
            # "dlc": dlc
            
        }


    with open("info.json", "w", encoding="utf-8") as f:
        json.dump(games_dict, f,indent=4, ensure_ascii=False)


    # with open("index.html", "w", encoding="utf-8") as f:
    #     f.write(str(soup))



if __name__ == "__main__":
    main()