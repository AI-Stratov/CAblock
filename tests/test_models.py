"""Class for testing models of the application."""
from datetime import datetime

from app import models


class TestModels:
    """Class for testing models of the application."""

    def test_request(self, test_session):
        """Check that model Request can be created correctly."""
        request = models.Request(
            id=10,
            is_resident=True,
            inn="1234567890",
            ogrn="9876543212345",
            in_sap=False,
            sap_num=None,
            mdm_id="mdm123",
            blocking=False,
            from_system=1,
            created_at=datetime.now(),
            created_by="test_user",
            approved_at=None,
            approved_by=None,
            start_at=datetime(2023, 1, 1),
            end_at=datetime(2023, 12, 31, 23, 59, 59),
            description="Testing request model",
        )

        test_session.add(request)
        test_session.commit()

        saved_request = (
            test_session.query(models.Request)
            .filter_by(inn="1234567890")
            .first()
        )

        assert saved_request is not None
        assert saved_request.is_resident is True
        assert saved_request.inn == "1234567890"
        assert saved_request.ogrn == "9876543212345"
        assert saved_request.in_sap is False
        assert saved_request.sap_num is None
        assert saved_request.mdm_id == "mdm123"
        assert saved_request.blocking is False
        assert saved_request.from_system == 1
        assert saved_request.created_at is not None
        assert saved_request.created_by == "test_user"
        assert saved_request.approved_at is None
        assert saved_request.approved_by is None
        assert saved_request.start_at == datetime(2023, 1, 1)
        assert saved_request.end_at == datetime(2023, 12, 31, 23, 59, 59)
        assert saved_request.description == "Testing request model"

    def test_dict_action(self, test_session):
        """Check that model DictAction can be created correctly."""
        action = models.DictAction(
            code=6,
            name="test_action",
        )

        test_session.add(action)
        test_session.commit()

        saved_action = (
            test_session.query(models.DictAction).filter_by(code=6).first()
        )

        assert saved_action is not None
        assert saved_action.code == 6
        assert saved_action.name == "test_action"

    def test_dict_doc_type(self, test_session):
        """Check that model DictDocType can be created correctly."""
        type = models.DictDocType(
            code=6,
            name="test_doc_type",
            fullname="test_doc_type_fullname",
            system_code=2,
        )

        test_session.add(type)
        test_session.commit()

        saved_type = (
            test_session.query(models.DictDocType).filter_by(code=6).first()
        )

        assert saved_type is not None
        assert saved_type.code == 6
        assert saved_type.name == "test_doc_type"
        assert saved_type.fullname == "test_doc_type_fullname"
        assert saved_type.system_code == 2

    def test_dict_operation(self, test_session):
        """Check that model DictOperation can be created correctly."""
        system = models.DictOperation(
            sap_code="S3",
            sap_name="test_system",
            name="test_name",
            blocking=True,
        )

        test_session.add(system)
        test_session.commit()

        saved_system = (
            test_session.query(models.DictOperation)
            .filter_by(sap_code="S3")
            .first()
        )

        assert saved_system is not None
        assert saved_system.sap_code == "S3"
        assert saved_system.sap_name == "test_system"
        assert saved_system.name == "test_name"

    def test_dict_system(self, test_session):
        """Check that model DictSystem can be created correctly."""
        system = models.DictSystem(
            code=4,
            name="test_system",
            can_block=True,
            source_doc=False,
        )

        test_session.add(system)
        test_session.commit()

        saved_system = (
            test_session.query(models.DictSystem).filter_by(code=4).first()
        )

        assert saved_system is not None
        assert saved_system.code == 4
        assert saved_system.name == "test_system"
        assert saved_system.can_block is True
        assert saved_system.source_doc is False

    def test_dict_workflow(self, test_session):
        """Check that model DictWorkflow can be created correctly."""
        workflow = models.DictWorkflow(
            code="PART",
            name="test_workflow",
        )

        test_session.add(workflow)
        test_session.commit()

        saved_workflow = (
            test_session.query(models.DictWorkflow)
            .filter_by(code="PART")
            .first()
        )

        assert saved_workflow is not None
        assert saved_workflow.code == "PART"
        assert saved_workflow.name == "test_workflow"

    def test_request_detail(self, test_session):
        """Check that model RequestDetail can be created correctly."""
        request_detail = models.RequestDetail(
            id=10,
            request_id=10,
            workflow_code="PART",
            params={"test": "test"},
        )

        test_session.add(request_detail)
        test_session.commit()

        saved_request_detail = (
            test_session.query(models.RequestDetail).filter_by(id=10).first()
        )

        assert saved_request_detail is not None
        assert saved_request_detail.id == 10
        assert saved_request_detail.request_id == 10
        assert saved_request_detail.workflow_code == "PART"
        assert saved_request_detail.params == {"test": "test"}
