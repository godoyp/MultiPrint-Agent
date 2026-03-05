# modules/schemas/error_schema.py
from marshmallow import Schema, fields

class ErrorDetailSchema(Schema):
    code = fields.Integer(required=True)
    status = fields.String(required=True)
    message = fields.String(required=True)
    errors = fields.Dict(allow_none=True)

class ErrorResponseSchema(Schema):
    success = fields.Boolean(required=True, dump_default=False)
    data = fields.Dict(allow_none=True)
    error = fields.Nested(ErrorDetailSchema, required=True)