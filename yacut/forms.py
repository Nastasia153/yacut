from flask_wtf import FlaskForm
from wtforms import URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from .constants import REGEXP


class URLForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Новая короткая ссылка',
        validators=[
            Regexp(REGEXP, flags=0,
                   message='Допускаются цифры, буквы латинского алфавита'),
            Length(6, 16, message='От 6 до 16 символов'), Optional()]
    )
