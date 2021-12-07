import json

def get_list_from_json(jsonfile):
    """
    преобразовываем json файл в list и добавляем большую букву в имени
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
    :return: bool
    """

    for dict in list:
        dict["poster_name"] = dict["poster_name"].title()
    return True


#print(add_count_comments(get_list_from_json("data/data.json"), get_list_from_json("data/comments.json")))
#print(get_true_word_form(1001))