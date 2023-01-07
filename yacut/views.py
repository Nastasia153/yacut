import secrets
import string

from flask import render_template, redirect, flash

from . import yacut, db
from .forms import URLForm
from .models import URLMap
from .constants import MAX_LENGTH


def get_unique_short_id(length):
    create_rand_link = string.ascii_letters + string.digits
    link = ''.join(secrets.choice(create_rand_link) for i in range(length))
    return link


@yacut.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        original_url = form.original_link.data
        short_url = form.custom_id.data
        if len(short_url) < 1:
            short_url = get_unique_short_id(MAX_LENGTH)
        if URLMap.query.filter_by(short=short_url).first() is not None:
            flash(f'Имя "{short_url}" уже занято!')
            return render_template('index.html', form=form)
        url = URLMap(
            original=original_url,
            short=short_url
        )
        context = {
            'form': form,
            'short_url': short_url
        }
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', **context)
    return render_template('index.html', form=form)


@yacut.route('/<string:short_url>/', methods=['GET'])
def redirect_short_url(short_url):
    url = URLMap.query.filter_by(short=short_url).first()
    if not url:
        return render_template('404.html')
    return redirect(url.original), 302
