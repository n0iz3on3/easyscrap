from fake_headers import Headers
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
import re

# задаем ключевые слова для поиска
KEYWORDS = ['схема', 'hard', 'Kotlin', 'Маск', 'Финансы', 'Точка', 'Python*', 'Cloud', 'Python', 'Rust']
keywords_pattern = '|'.join([f"\\b{word}\\b" for word in KEYWORDS])

# получаем страницу с самыми свежими постами
url = 'https://habr.com/ru/all/'
headers = Headers(headers=True).generate()
response = get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# формируем результирующую выборку
def get_result(post):
    date_time = post.find('time').get('title')
    title_text = post.find('h2').find('span').text
    link = post.find('h2').find('a').get('href')
    full_link = f'https://habr.com{link}'
    return f'<{date_time}> - <{title_text}> - <{full_link}>'

# извлекаем посты, хабы, заголовки
article = soup.find_all('article')
sleep(0.33)
def get_posts(article, keywords):
    result = set()
    for post in tqdm(article, desc='Preparing results'):
        # заголовок
        title_text = post.find('h2').find('span').text
        if re.search(keywords, title_text, flags=re.I):
            result.add(get_result(post))

        sleep(0.33)     
        # хабы (хэштэги)
        hubs = post.find_all(class_="tm-article-snippet__hubs-item")
        hubs = [hub.text.strip() for hub in hubs]
        for hub in hubs:
            if re.search(keywords, hub, flags=re.I):
                result.add(get_result(post))

        sleep(0.33)
        # текст превью
        post_text = post.find_all('p')
        post_text = [post.text.strip() for post in post_text]
        for raw in post_text:
            if re.search(keywords, raw, flags=re.I):
                result.add(get_result(post))

    return result

scrap_results = get_posts(article, keywords_pattern)