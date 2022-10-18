import logging

from db import db
from flask import Blueprint, jsonify, abort
from apps.posts.dao.post_dao import PostDAO
from apps.comments.dao.comment_dao import CommentDAO

# Создаем блупринт
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS

bp_api = Blueprint("bp_api", __name__)

posts_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)

api_logger = logging.getLogger("api_logger")


@bp_api.route("/")
def api_posts_hello():
    return "Это апи. Доступные эндпоинты /api/posts и /api/posts/pk"


@bp_api.route("/posts/")
def api_posts_all():
    """ Эндпоинт для всех постов"""
    all_posts = posts_dao.get_all()
    all_posts_as_dict = [post.as_dict() for post in all_posts]

    api_logger.debug("Запрошены все посты")

    return jsonify(all_posts_as_dict), 200


@bp_api.route("/posts/<int:pk>/")
def api_post_single(pk):
    """ Эндпоинт для одного поста"""
    post = posts_dao.get_post_by_pk(pk)
    if post is None:
        api_logger.debug(f"Обращение к несуществующему посту {pk}")
        abort(404)

    api_logger.debug(f"Запрошен пост {pk}")

    return jsonify(post.as_dict()), 200


@bp_api.route("/test_db")
def test_db():
    result = db.session.execute(
        'SELECT 17'
    ).scalar()

    return jsonify(
        {
            'result': result,
        }
    )


@bp_api.errorhandler(404)
def api_error_404(error):
    api_logger.error(f"Ошибка {error}")
    return jsonify({"error": str(error)}), 404
