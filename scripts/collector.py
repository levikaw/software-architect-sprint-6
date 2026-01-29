from bs4 import BeautifulSoup
import requests
import os
import json

# персонажи из вселенной Теории большого взрыва
characters = [
    'Sheldon_Cooper', 
    'Amy_Farrah_Fowler', 
    'Leonard_Hofstadter', 
    'Penny', 
    'Howard_Wolowitz', 
    'Rajesh_Koothrappali', 
    'Bernadette_Rostenkowski-Wolowitz',
    ]

# урл для получения информации 
base_url = 'https://bigbangtheory.fandom.com/wiki/'

def get_html_doc(character_name: str) -> str:
    """ получение html """
    response = requests.get(base_url + character_name)

    if response.status_code == 200:
        return response.text

def parse_html(html_text: str) -> str: 
    """
    получения текста из <div id="content">
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    div = soup.find('div', id='content', recursive=True) 
    text_content = div.get_text().strip() 

    return text_content

def replace_names(text_content: str, reverse=False) -> str:
    """ 
    замена имен

    - имена разбиты на токены и заменяются отдельно
    """
    path = os.path.join('terms_map.json')
    with open(path, 'r') as dict_file:
        terms_map = json.load(dict_file)
        
        for original_name in terms_map:
            if reverse:
                text_content = text_content.replace(terms_map[original_name], original_name)
            else:
                text_content = text_content.replace(original_name, terms_map[original_name])

    return text_content     


def save_knowledge_base(file_name: str, text_content: str):
    """ сохранение в базу знаний """
    directory = 'knowledge_base'

    if not os.path.exists(directory):
      os.makedirs(directory)

    path = os.path.join(directory, file_name + '.txt')
    with open(path, 'w') as file:
        file.write(text_content)

if __name__ == '__main__':
    for character in characters:
        content = get_html_doc(character)
        text = parse_html(content)

        # заменяем различные вспомогательные символы страниц
        # и берем только раздел Biography
        text = text.replace('[]', '').replace('\n', ' ').strip().split('Biography')[2]

        text = replace_names(text, False)

        save_knowledge_base(character, text)