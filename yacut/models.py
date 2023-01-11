from datetime import datetime

from yacut import db
from yacut.constants import HOST


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=f'http://{HOST}/{self.short}',
        )

    def from_dict(self, data):
        api_dict = {
            'original': 'url',
            'short': 'custom_id'
        }
        for field in api_dict.keys():
            if api_dict[field] in data:
                setattr(self, field, data[api_dict[field]])
