from datetime import datetime

from yacut import db

FIELDS = {'original': 'url', 'short': 'custom_id'}


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(128), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            cshort_link=self.short,
        )

    def from_dict(self, data):
        for field in FIELDS.keys():
            if field in data:
                setattr(self, field, data[field])
