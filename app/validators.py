"""Validators for schemas."""
from pydantic import BaseModel, root_validator, validator
import app.helpers as h

class BaseSchema(BaseModel):
    """Base schema for inheritance."""

    @root_validator(pre=True, allow_reuse=True)
    def validate_fields(cls, values):
        return h.validate_fields(values)

    @validator("end_at", check_fields=False)
    def validate_end_at(cls, end_at, values):
        return h.validate_end_at(end_at, values)

    @validator("approved_at", check_fields=False)
    def validate_approved_at(cls, approved_at, values):
        return h.validate_approved_at(approved_at, values)

    @validator("approved_by", check_fields=False)
    def validate_approved_by(cls, approved_by, values):
        return h.validate_approved_by(approved_by, values)


class BaseWorkflowParams(BaseModel):
    """Base class for workflow params."""

    @validator("params", check_fields=False)
    def validate_params(cls, params, values):
        return h.validate_params(params, values)
