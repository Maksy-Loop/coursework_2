import json

def get_list_from_json(jsonfile):
    """
    преобразовываем json файл в list
    :param jsonfile:
    :return: list
    """
    with open(jsonfile, "r") as f:

        json_list = json.load(f)

    return json_list


def cut_50_symbol(data):
    """
    Данная функция обрезает текст до 50 символов
    :param data:
    :return:
    """
    for dict in data:
        dict["content"] = dict["content"][0:49] + "..."

    return data

def add_count_comments(data, commentsdata):
    """
    функиця считает коментарии по каждому посту и добавляет их в словарь
    :param data: list
    :param commentsdata: list
    :return: bool
    """
    for dict_data in data:
        count = 0
        for dict_commentsdata in commentsdata:

            if dict_data["pk"] == dict_commentsdata["post_id"]:
                count += 1

        dict_data["count_comments"] = f'{count} {get_true_word_form(count)}'

    return True

def get_true_word_form(number):
    """
    функция приводит слово в правильную форму в зависомости от количества единиц
    :param number:
    :return: str
    """
    if 11 <= number < 20 or number % 10 == 0:
        return "комментариев"
    elif number % 10 == 1:
        return "комментарий"
    elif 2 <= number % 10 <= 4:
        return "комментария"
    else:
        return "комментариев"

def do_title_name(list):
    """
    Функция преобразовывает первую букву в имени в большую
    :param list:
    :return: list
    """

    for dict in list:
        dict["poster_name"] = dict["poster_name"].title()
    return list


def search_post_by_word(list, word ):
    """
    функция перебирает словарь и генериует новый список со свавариями, которые имеют нужное нам вхождение в тесте
    :param list:
    :param word: str
    :return: list
    """
    ten_post_list = []
    for ditc in list:

        if word.lower() in ditc.get("content").lower():
            ten_post_list.append(ditc)
            if len(ten_post_list) == 10:
                break

    return ten_post_list


def sort_post_by_poster_name(data, poster_name):
    """
    функция фильтрует и возвращает список только с определенным poster_name
    :param data: list
    :param poster_name: str
    :return: list
    """
    data_new = []
    for dict in data:
        if dict["poster_name"].lower() == poster_name:
            data_new.append(dict)

    return data_new

def add_tag_link(data):
    for dict in data:
        text = dict["content"].split(" ")
        for j, word in enumerate(text):
            if word.startswith("#"):
                word = word.replace("#", "")
                text[j] = f'<a href="/tag/{word}">#{word}</a>'

        dict["content"] = " ".join(text)

    return data


def add_value(list, jsonfile):
    """
    функция перезаписывает json файл
    :param dict:
    :param json:
    :return: bool
    """
    with open(jsonfile, "w") as f:
        json.dump(list, f, ensure_ascii=False, indent=4)

    return True


def seach_post_by_tag(data, tag):
    """
    функция которая формирует список словарей только если в тексте есть тег
    :param data:
    :param tag:
    :return:
    """
    tag = f'#{tag}'
    new_data = []
    for dict in data:
        if tag.lower() in dict["content"].lower():
            new_data.append(dict)

    return new_data

#print(add_count_comments(get_list_from_json("data/data.json"), get_list_from_json("data/comments.json")))
#print(get_true_word_form(1001))
#a = "На следующий день"
#print(search_post_by_word((get_list_from_json("data/data.json")), a))
#print(sort_post_by_poster_name(get_list_from_json("data/data.json"), "leo"))
#print(add_tag_link(get_list_from_json("data/data.json")))
#print(seach_post_by_tag(get_list_from_json("data/data.json"), "кот"))