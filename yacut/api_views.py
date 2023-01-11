from re import fullmatch

from flask import jsonify, request

from yacut import app, db
from yacut.constants import MAX_LENGTH, REGEXP
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = data['custom_id'] = get_unique_short_id(MAX_LENGTH)
    is_match = fullmatch(REGEXP, custom_id)
    if not is_match:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if len(custom_id) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
