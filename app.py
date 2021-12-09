from flask import Flask, request, render_template, send_from_directory, redirect, abort
from functions import get_list_from_json, cut_50_symbol, add_count_comments, do_title_name, search_post_by_word, sort_post_by_poster_name, add_tag_link, add_value, seach_post_by_tag

DATA_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"
BOOKMARKS_PATH = "data/bookmarks.json"
IMG_FOLDER = "imgloads/img"

app = Flask(__name__)


@app.route("/")
def page_index():
    data = cut_50_symbol(do_title_name(add_tag_link(get_list_from_json(DATA_PATH))))
    comments = get_list_from_json(COMMENTS_PATH)
    add_count_comments(data, comments)
    bookmarks_list = get_list_from_json(BOOKMARKS_PATH)
    return render_template('index.html',  data = data, count_bookmarks = len(bookmarks_list))


@app.route('/post/<int:id>/', methods = ["POST", "GET"])
def page_post(id):
    data = do_title_name(add_tag_link(get_list_from_json(DATA_PATH)))
    comments = get_list_from_json(COMMENTS_PATH)
    add_count_comments(data, comments)

    for i in data:
        if id == i["pk"]:
            postid = i.get("pk")
            username = i.get("poster_name")
            avatar = i.get("poster_avatar")
            picture = i.get("pic")
            content = i.get("content")
            views_count = i.get("views_count")
            count_comments = i.get("count_comments")

            if request.method == "POST":

                name = request.form.get("name_commentator")
                comment = request.form.get("comment")

                if name and comment:

                    comments = get_list_from_json(COMMENTS_PATH)

                    dict_comment = {
                                        "post_id": postid,
                                        "commenter_name": name,
                                        "comment": comment,
                                        "pk": len(comments) + 1
                                    }

                    comments.append(dict_comment)
                    add_value(comments, COMMENTS_PATH)

                abort(400)

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
        search_posts = search_post_by_word(add_tag_link(cut_50_symbol(do_title_name(get_list_from_json(DATA_PATH)))), search_word)
        comments = get_list_from_json(COMMENTS_PATH)
        add_count_comments(search_posts, comments)


        return render_template("search.html", search_posts = search_posts, count_posts = len(search_posts), search_word = search_word)


@app.route('/users/<username>')
def page_user_post(username):
    data = cut_50_symbol(do_title_name(add_tag_link(get_list_from_json(DATA_PATH))))
    comments = get_list_from_json(COMMENTS_PATH)
    add_count_comments(data, comments)
    data = sort_post_by_poster_name(data, username)

    if len(data) >= 1:
        return render_template('user-feed.html', data = data, username = username)

    abort(404)


@app.route('/bookmarks/add/<int:postid>')
def add_post_to_bookmarks(postid):
    data = cut_50_symbol(do_title_name(add_tag_link(get_list_from_json(DATA_PATH))))
    comments = get_list_from_json(COMMENTS_PATH)
    add_count_comments(data, comments)
    bookmarks_list = get_list_from_json(BOOKMARKS_PATH)

    for dict in data:
        if postid == dict.get("pk"):
            if dict not in bookmarks_list:
                bookmarks_list.append(dict)
                add_value(bookmarks_list, BOOKMARKS_PATH)

                return redirect("/", code = 302)

    abort(400)


@app.route('/bookmarks/remove/<int:postid>')
def del_post_from_bookmarks(postid):

    bookmarks_list = get_list_from_json(BOOKMARKS_PATH)

    for dict in bookmarks_list:
        if postid == dict.get("pk"):
            bookmarks_list.remove(dict)
            add_value(bookmarks_list, BOOKMARKS_PATH)
            return redirect("/", code = 302)

    abort(400)


@app.route("/bookmarks")
def page_bookmarks():
    bookmarks_list = get_list_from_json(BOOKMARKS_PATH)
    return render_template('bookmarks.html',  bookmarks = bookmarks_list)

@app.route('/tag/<tagname>')
def page_search_tag(tagname):
    data_list = cut_50_symbol(do_title_name(add_tag_link(get_list_from_json(DATA_PATH))))
    comments = get_list_from_json(COMMENTS_PATH)
    add_count_comments(data_list, comments)
    data = seach_post_by_tag(data_list, tagname)
    if len(data) >= 1:
        return render_template('tag.html', data = data, tag = tagname)
    abort(404)


app.run()