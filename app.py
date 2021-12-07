from flask import Flask, request, render_template, send_from_directory, redirect, abort
from functions import get_list_from_json, cut_50_symbol, add_count_comments, do_title_name

DATA_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"
BOOKMARKS_PATH = "data/bookmarks.json"
IMG_FOLDER = "imgloads/img"

app = Flask(__name__)


@app.route("/")
def page_index():
    data = cut_50_symbol(get_list_from_json(DATA_PATH))
    comments = get_list_from_json(COMMENTS_PATH)
    add_count_comments(data, comments)
    do_title_name(data)
    return render_template('index.html',  data = data)


@app.route("/tag")
def page_tag():
    pass
    #поиск по слову = request.args.get("tag")
    #if tagname is None:
    #    abort(404)
    #else:


@app.route("/imgloads/<path:path>")
def static_dir(path):
    return send_from_directory(IMG_FOLDER, path)


app.run()