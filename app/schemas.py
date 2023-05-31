"""Schemas for request body validation."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, conlist, constr

from app.validators import BaseSchema, BaseWorkflowParams


class WorkflowParams(BaseWorkflowParams):
    """Workflow params."""

    max_sum: Optional[int]
    operation_sap_code: Optional[conlist(str, max_items=4)]
    balance_unit: Optional[constr(max_length=5)]
    system_code: Optional[int]
    doc_type_code: Optional[int]
    action_code: Optional[int]
    doc_num: Optional[str]
    name_object: Optional[str]
    contract: Optional[str]
    debit: Optional[bool]
    account: Optional[constr(max_length=10)]


class RequestDetail(BaseWorkflowParams):
    """Request detail."""

    workflow_code: str
    params: WorkflowParams


class BlockRequest(BaseSchema):
    """Block request schema."""

    is_resident: bool
    inn: Optional[constr(max_length=60)]
    ogrn: Optional[constr(max_length=60)]
    in_sap: bool
    sap_num: Optional[constr(max_length=20)]
    mdm_id: Optional[constr(max_length=20)]
    from_system: int
    created_by: constr(max_length=30)
    approved_at: Optional[datetime]
    approved_by: Optional[constr(max_length=30)]
    start_at: datetime = datetime(1990, 1, 1)
    end_at: datetime = datetime(9999, 12, 31, 23, 59, 59)
    description: Optional[str]
    details: List[RequestDetail]


class CheckRequest(BaseSchema):
    """Check request schema."""

    from_system: int
    employee: constr(max_length=20)
    inn: Optional[constr(max_length=60)]
    ogrn: Optional[constr(max_length=60)]
    sap_num: Optional[constr(max_length=20)]
    contract: Optional[constr(max_length=60)]
    check_for_dt: Optional[datetime]


class BlockResponse(BaseModel):
    """Block response schema."""

    request_id: int
    reg_datetime: datetime


class CheckResponse(BaseModel):
    """Check response schema."""

    blocking: bool


class DictOperation(BaseModel):
    """Dict operation schema."""

    sap_code: str
    sap_name: str
    name: str


class DictSystemSchema(BaseModel):
    code: int
    name: str


class DictDocTypeSchema(BaseModel):
    code: int
    name: str
    fullname: str


class DictActionCodeSchema(BaseModel):
    """Dict action code schema."""

    code: int
    name: str

