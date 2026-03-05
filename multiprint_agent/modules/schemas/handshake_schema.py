from marshmallow import Schema, fields
from .error_schema import ErrorDetailSchema

class HandshakeDataSchema(Schema):
    token = fields.String(required=True)
    expires_in = fields.Integer(required=True)

class HandshakeResponseSchema(Schema):
    success = fields.Boolean(required=True)
    data = fields.Nested(HandshakeDataSchema, required=True)
    error = fields.Nested(ErrorDetailSchema, allow_none=True)