from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from yacut.constants import REGEXP


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Regexp(REGEXP, flags=0,
                   message='Допускаются цифры, буквы латинского алфавита'),
            Length(2, 16, message='От 6 до 16 символов'), Optional()]
    )
