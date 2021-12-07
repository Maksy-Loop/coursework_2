from flask import Flask, request, render_template, send_from_directory, redirect, abort
from functions import get_list_from_json, cut_50_symbol, add_count_comments, do_title_name, search_post_by_word

DATA_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"
BOOKMARKS_PATH = "data/bookmarks.json"
IMG_FOLDER = "imgloads/img"

app = Flask(__name__)


@app.route("/")
def page_index():
    data = cut_50_symbol(do_title_name(get_list_from_json(DATA_PATH)))
    comments = get_list_from_json(COMMENTS_PATH)
    add_count_comments(data, comments)
    return render_template('index.html',  data = data)


@app.route('/post/<int:id>/')
def page_candidate(id):
    data = do_title_name(get_list_from_json(DATA_PATH))
    comments = get_list_from_json(COMMENTS_PATH)
    add_count_comments(data, comments)

    for i in data:
        if id == i["pk"]:
            postid = i["pk"]
            username = i.get("poster_name")
            avatar = i.get("poster_avatar")
            picture = i.get("pic")
            content = i.get("content")
            views_count = i.get("views_count")
            count_comments = i.get("count_comments")

            return render_template('post.html', username = username, avatar = avatar, picture=picture, content = content,
                                  views_count = views_count, count_comments = count_comments, postid = postid,
                                   comments = comments)

    abort(404)


@app.route("/search")
def page_search():
    search_word = request.args.get("s")
    if search_word is None:
        abort(404)

    else:
        search_posts = search_post_by_word(cut_50_symbol(do_title_name(get_list_from_json(DATA_PATH))), search_word)
        comments = get_list_from_json(COMMENTS_PATH)
        add_count_comments(search_posts, comments)


        return render_template("search.html", search_posts = search_posts, count_posts = len(search_posts), search_word = search_word)




app.run()