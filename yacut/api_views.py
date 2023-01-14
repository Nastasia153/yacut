from http import HTTPStatus
from re import fullmatch

from flask import jsonify, request

import yacut.constants as const
from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import check_url, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(const.NO_REQUEST_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(const.NO_REQUIRED_FIELD)
    custom_id = data.get('custom_id')
    if not custom_id:
        custom_id = data['custom_id'] = get_unique_short_id(const.MAX_LENGTH)
    is_match = fullmatch(const.REGEXP, custom_id)
    if not is_match or len(custom_id) > const.MAX_LEN_CUSTOM_ID:
        raise InvalidAPIUsage(const.INVALID_ARG_NAME)
    if check_url(custom_id) is not None:
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')

    url = URLMap()
    url.from_dict(data)
    URLMap.add_url_map(url)
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = check_url(short_id)
    if url is None:
        raise InvalidAPIUsage(const.NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
