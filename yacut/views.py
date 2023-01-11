import secrets
import string

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.constants import MAX_LENGTH
from yacut.forms import URLForm
from yacut.models import URLMap


def get_unique_short_id(length):
    create_rand_link = string.ascii_letters + string.digits
    link = ''.join(secrets.choice(create_rand_link) for i in range(length))
    return link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        original_url = form.original_link.data
        short_url = form.custom_id.data
        if not short_url:
            short_url = get_unique_short_id(MAX_LENGTH)
        if URLMap.query.filter_by(short=short_url).first() is not None:
            flash(f'Имя {short_url} уже занято!')
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


@app.route('/<string:short_url>', methods=['GET'])
def redirect_short_url(short_url):
    url = URLMap.query.filter_by(short=short_url).first()
    if not url:
        abort(404)
    return redirect(url.original), 302
