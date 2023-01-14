import secrets
import string

from yacut.models import URLMap


def get_unique_short_id(length):
    create_rand_link = string.ascii_letters + string.digits
    link = ''.join(secrets.choice(create_rand_link) for i in range(length))
    return link


def check_url(arg):
    return URLMap.query.filter_by(short=arg).first()
