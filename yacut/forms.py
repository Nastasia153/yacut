from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

import yacut.constants as const


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message=const.FORM_REQUIRED_FIELD)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Regexp(const.REGEXP, flags=0,
                   message=const.FORM_HELP_MSG),
            Length(1, const.MAX_LEN_CUSTOM_ID, message=const.FORM_LEN_MSG),
            Optional()
        ]
    )
