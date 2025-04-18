from marshmallow import Schema, fields

class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
