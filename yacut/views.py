from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut import app
from yacut.constants import MAX_LENGTH
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import check_url, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    if form.validate_on_submit():
        original_url = form.original_link.data
        short_url = form.custom_id.data
        if not short_url:
            short_url = get_unique_short_id(MAX_LENGTH)
        if check_url(short_url) is not None:
            flash(f'Имя {short_url} уже занято!')
            return render_template('index.html', form=form)
        url = URLMap(
            original=original_url,
            short=short_url
        )
        URLMap.add_url_map(url)
        context = {
            'form': form,
            'short_url': short_url
        }
        return render_template('index.html', **context)
    return render_template('index.html', form=form)


@app.route('/<string:short_url>', methods=['GET'])
def redirect_short_url(short_url):
    url = check_url(short_url)
    if not url:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url.original), HTTPStatus.FOUND
