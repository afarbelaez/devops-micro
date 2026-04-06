from marshmallow import Schema, fields, validate


class BlacklistEntryInputSchema(Schema):
    email = fields.Email(required=True)
    app_uuid = fields.String(required=True)
    blocked_reason = fields.String(
        required=False,
        load_default=None,
        validate=validate.Length(max=255)
    )


class BlacklistEntryOutputSchema(Schema):
    isBlacklisted = fields.Boolean()
    blockedReason = fields.String(allow_none=True)
