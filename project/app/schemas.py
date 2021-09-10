from marshmallow import EXCLUDE, Schema, fields


class ExcludeSchema(Schema):
    """Excluded all unknown fields"""

    class Meta:
        unknown = EXCLUDE


class TickerSchema(ExcludeSchema):
    ticker = fields.Str(required=True, allow_none=False)
