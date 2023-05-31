import pytest
import app.helpers as h


class TestValidators:
    def test_validate_fields(self):
        """Should raise ValueError with the correct error message."""

        with pytest.raises(ValueError) as exc_info:
            h.validate_fields({"inn": "", "ogrn": "", "sap_num": ""})
        assert str(exc_info.value) == "Either INN or OGRN or SAP_NUM must be provided"

        with pytest.raises(ValueError) as exc_info:
            h.validate_fields({"inn": "123456789", "is_resident": True})
        assert str(exc_info.value) == "Invalid INN length for residents"

        with pytest.raises(ValueError) as exc_info:
            h.validate_fields({"inn": "aaaaaaaaaa", "is_resident": True})
        assert str(exc_info.value) == "Invalid INN format (not digits) for residents"

        with pytest.raises(ValueError) as exc_info:
            h.validate_fields({"inn": ''.join([str(x) for x in range(1, 61)]), "is_resident": False})
        assert str(exc_info.value) == "Invalid INN length for non-residents"

        with pytest.raises(ValueError) as exc_info:
            h.validate_fields({"ogrn": "123456789", "is_resident": True})
        assert str(exc_info.value) == "Invalid OGRN length for residents"

        with pytest.raises(ValueError) as exc_info:
            h.validate_fields({"ogrn": "aaaaaaaaaaaaa", "is_resident": True})
        assert str(exc_info.value) == "Invalid OGRN format (not digits) for residents"

        with pytest.raises(ValueError) as exc_info:
            h.validate_fields({"ogrn": ''.join([str(x) for x in range(1, 61)]), "is_resident": False})
        assert str(exc_info.value) == "Invalid OGRN length for non-residents"


def test_validate_end_at():
    """Should raise ValueError with the correct error message."""

    with pytest.raises(ValueError) as exc_info:
        h.validate_end_at(1, {"start_at": 2})
    assert str(exc_info.value) == "end_at must be greater than or equal to start_at"


def test_validate_approved_at():
    """Should raise ValueError with the correct error message."""

    with pytest.raises(ValueError) as exc_info:
        h.validate_approved_at(None, {"blocking": False})
    assert str(exc_info.value) == "approved_at is required when blocking is False"


def test_validate_approved_by():
    """Should raise ValueError with the correct error message."""

    with pytest.raises(ValueError) as exc_info:
        h.validate_approved_by(None, {"blocking": False})
    assert str(exc_info.value) == "approved_by is required when blocking is False"


def test_validate_params():
    """Should raise ValueError with the correct error message."""

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(doc_type_code=None), {"workflow_code": "DOC", "blocking": True})
    assert str(exc_info.value) == "workflow_code DOC is not allowed when blocking is True"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(max_sum=None), {"workflow_code": "SUM"})
    assert str(exc_info.value) == "max_sum is required for SUM workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(operation_sap_code=None), {"workflow_code": "OPER"})
    assert str(exc_info.value) == "operation_sap_code is required for OPER workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(balance_unit=None), {"workflow_code": "UNIT"})
    assert str(exc_info.value) == "balance_unit is required for UNIT workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(system_code=""), {"workflow_code": "DOC"})
    assert str(exc_info.value) == "system_code is required for DOC workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(doc_type_code=None), {"workflow_code": "DOC"})
    assert str(exc_info.value) == "doc_type_code is required for DOC workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(doc_type_code=1, action_code=None), {"workflow_code": "DOC"})
    assert str(exc_info.value) == "action_code is required for DOC workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(doc_type_code=1, action_code=1, doc_num=None), {"workflow_code": "DOC"})
    assert str(exc_info.value) == "doc_num is required for DOC workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(doc_type_code=3, action_code=1, doc_num=1, name_object=None), {"workflow_code": "DOC"})
    assert str(exc_info.value) == "name_object is required for DOC workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(doc_type_code=4, action_code=1, doc_num=1, contract=None), {"workflow_code": "DOC"})
    assert str(exc_info.value) == "contract is required for DOC workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(debit=None), {"workflow_code": "ACC"})
    assert str(exc_info.value) == "debit is required for ACC workflow"

    with pytest.raises(ValueError) as exc_info:
        h.validate_params(Params(debit=True, account=None), {"workflow_code": "ACC"})
    assert str(exc_info.value) == "account is required for ACC workflow"


class Params:
    def __init__(
        self,
        max_sum=None,
        operation_sap_code=None,
        balance_unit=None,
        system_code=None,
        doc_type_code=None,
        action_code=None,
        doc_num=None,
        name_object=None,
        contract=None,
        debit=None,
        account=None,
    ):
        self.max_sum = max_sum
        self.operation_sap_code = operation_sap_code
        self.balance_unit = balance_unit
        self.system_code = system_code
        self.doc_type_code = doc_type_code
        self.action_code = action_code
        self.doc_num = doc_num
        self.name_object = name_object
        self.contract = contract
        self.debit = debit
        self.account = account