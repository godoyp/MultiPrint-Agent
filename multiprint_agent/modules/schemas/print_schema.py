from marshmallow import Schema, fields
from .error_schema import ErrorDetailSchema

class PrintRequestSchema(Schema):
    mode = fields.String(required=False, allow_none=True)
    raw = fields.String(required=False)
    contentType = fields.String(required=False)
    encoding = fields.String(required=False)

class PrintDataSchema(Schema):
    mode = fields.String(required=True)
    raw = fields.String(allow_none=True)
    contentType = fields.String(allow_none=True)
    encoding = fields.String(allow_none=True)

class PrintResponseSchema(Schema):
    success = fields.Boolean(required=True)
    data = fields.Nested(PrintDataSchema, required=True)
    error = fields.Nested(ErrorDetailSchema, allow_none=True)