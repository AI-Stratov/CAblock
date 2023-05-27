"""Validators for schemas."""
from pydantic import BaseModel, root_validator, validator


class BaseSchema(BaseModel):
    """Base schema for inheritance."""

    @root_validator(pre=True, allow_reuse=True)
    def validate_fields(cls, values):
        """Root validation for cross validation."""
        inn = values.get("inn")
        ogrn = values.get("ogrn")
        sap_num = values.get("sap_num")
        is_resident = values.get("is_resident")
        if not inn and not ogrn and not sap_num:
            raise ValueError("Either INN or OGRN or SAP_NUM must be provided")
        if inn:
            if is_resident:
                if len(inn) not in [10, 12]:
                    raise ValueError("Invalid INN length for residents")
                if not inn.isdigit():
                    raise ValueError(
                        "Invalid INN format (not digits) for residents",
                    )
            else:
                if len(inn) > 60:
                    raise ValueError("Invalid INN length for non-residents")
        if ogrn:
            if is_resident:
                if len(ogrn) not in [13, 15]:
                    raise ValueError("Invalid OGRN length for residents")
                if not ogrn.isdigit():
                    raise ValueError(
                        "Invalid OGRN format (not digits) for residents",
                    )
            else:
                if len(ogrn) > 60:
                    raise ValueError("Invalid OGRN length for non-residents")
        if sap_num is not None:
            values["in_sap"] = True

        return values

    @validator("end_at", check_fields=False)
    def validate_end_at(cls, end_at, values):
        """Validate end_at field."""
        if "start_at" in values and end_at < values["start_at"]:
            raise ValueError(
                "end_at must be greater than or equal to start_at",
            )
        return end_at

    @validator("approved_at", check_fields=False)
    def validate_approved_at(cls, approved_at, values):
        """Validate approved_at field."""
        if (
            "blocking" in values
            and not values["blocking"]
            and approved_at is None
        ):
            raise ValueError("approved_at is required when blocking is False")
        return approved_at

    @validator("approved_by", check_fields=False)
    def validate_approved_by(cls, approved_by, values):
        """Validate approved_by field."""
        if (
            "blocking" in values
            and not values["blocking"]
            and approved_by is None
        ):
            raise ValueError("approved_by is required when blocking is False")
        return approved_by


class BaseWorkflowParams(BaseModel):
    """Base class for workflow params."""

    @validator("params", check_fields=False)
    def validate_params(cls, params, values):
        """Validate params field."""
        workflow_code = values.get("workflow_code")
        doc_type_code = params.doc_type_code
        blocking = values.get("blocking")
        if blocking and workflow_code == "DOC":
            raise ValueError(
                "workflow_code DOC is not allowed when blocking is True",
            )

        match workflow_code:
            case "FULL":
                pass
            case "SUM":
                if not params.max_sum:
                    raise ValueError("max_sum is required for SUM workflow")
            case "OPER":
                if not params.operation_sap_code:
                    raise ValueError(
                        "operation_sap_code is required for OPER workflow",
                    )
            case "UNIT":
                if not params.balance_unit:
                    raise ValueError(
                        "balance_unit is required for UNIT workflow",
                    )
            case "DOC":
                if params.system_code == "":
                    raise ValueError(
                        "system_code is required for DOC workflow",
                    )
                if not params.doc_type_code:
                    raise ValueError(
                        "doc_type_code is required for DOC workflow",
                    )
                if not params.action_code:
                    raise ValueError(
                        "action_code is required for DOC workflow",
                    )
                if not params.doc_num:
                    raise ValueError("doc_num is required for DOC workflow")
                if doc_type_code == 3:
                    if not params.name_object:
                        raise ValueError(
                            "name_object is required for DOC workflow",
                        )
                if doc_type_code == 4:
                    if not params.contract:
                        raise ValueError(
                            "contract is required for DOC workflow",
                        )
            case "ACC":
                if not params.debit:
                    raise ValueError("debit is required for ACC workflow")
                if not params.account:
                    raise ValueError("account is required for ACC workflow")

        return params
