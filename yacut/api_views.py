from flask import jsonify, request
from re import fullmatch

from . import yacut, db
from . models import URLMap
from . views import get_unique_short_id
from .error_handlers import InvalidAPIUsage
from .constants import MAX_LENGTH, REGEXP


@yacut.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if len(data['custom_id']) < 1:
        short_url = get_unique_short_id(MAX_LENGTH)
    else:
        short_url = data.get('custom_id')
    is_match = fullmatch(REGEXP, short_url)
    if not is_match:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if len(short_url) < 6 or len(short_url) > 16:
        raise InvalidAPIUsage('От 6 до 16 символов')
    if URLMap.query.filter_by(short=short_url).first() is not None:
        raise InvalidAPIUsage(f'Имя "{short_url}" уже занято')

    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@yacut.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
