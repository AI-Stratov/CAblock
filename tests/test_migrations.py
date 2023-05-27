"""Class for testing migrations in the database."""
from app import models


class TestMigrations:
    """Class for testing migrations in the database."""

    def test_dict_actions(self, test_session):
        """Check that dict_actions table is filled with correct data."""
        expected_actions = [
            {"code": 1, "name": "изменение"},
            {"code": 2, "name": "сторнирование"},
            {"code": 3, "name": "создать последующий"},
            {"code": 4, "name": "выравнивание"},
            {"code": 5, "name": "отмена выравнивания"},
        ]
        actual_actions = test_session.query(models.DictAction).all()
        assert len(actual_actions) == len(expected_actions)

        for expected_action in expected_actions:
            actual_action = (
                test_session.query(models.DictAction)
                .filter_by(code=expected_action["code"])
                .first()
            )
            assert actual_action is not None
            assert actual_action.name == expected_action["name"]

    def test_dict_doc_type(self, test_session):
        """Check that dict_doc_type table is filled with correct data."""
        expected_doc_types = [
            {
                "code": 1,
                "name": "FI",
                "fullname": "бухгалтерский документ",
                "system_code": 1,
            },
            {
                "code": 2,
                "name": "MM",
                "fullname": "заказ на закупку",
                "system_code": 1,
            },
            {
                "code": 3,
                "name": "CTR",
                "fullname": "договор (контракт)",
                "system_code": 2,
            },
            {
                "code": 4,
                "name": "ADD",
                "fullname": "дополнительное соглашение",
                "system_code": 2,
            },
        ]

        actual_doc_types = test_session.query(models.DictDocType).all()
        assert len(actual_doc_types) == len(expected_doc_types)

        for expected_doc_type in expected_doc_types:
            actual_doc_type = (
                test_session.query(models.DictDocType)
                .filter_by(code=expected_doc_type["code"])
                .first()
            )
            assert actual_doc_type is not None
            assert actual_doc_type.name == expected_doc_type["name"]
            assert actual_doc_type.fullname == expected_doc_type["fullname"]
            assert (
                actual_doc_type.system.code == expected_doc_type["system_code"]
            )

    def test_dict_system(self, test_session):
        """Check that dict_system table is filled with correct data."""
        expected_systems = [
            {
                "code": 0,
                "name": "Support.x5.ru",
                "can_block": True,
                "source_doc": False,
            },
            {
                "code": 1,
                "name": "SAP ERP",
                "can_block": False,
                "source_doc": True,
            },
            {"code": 2, "name": "СЭД", "can_block": False, "source_doc": True},
            {"code": 3, "name": "ESM", "can_block": True, "source_doc": False},
        ]

        actual_systems = test_session.query(models.DictSystem).all()
        assert len(actual_systems) == len(expected_systems)

        for expected_system in expected_systems:
            actual_system = (
                test_session.query(models.DictSystem)
                .filter_by(code=expected_system["code"])
                .first()
            )
            assert actual_system is not None
            assert actual_system.name == expected_system["name"]
            assert actual_system.source_doc == expected_system["source_doc"]

    def test_dict_type_valid_action(self, test_session):
        """Check that dict_type_valid_action table is filled with data."""
        expected_type_valid_actions = [
            {"doc_type_code": 1, "action_code": 1},
            {"doc_type_code": 1, "action_code": 2},
            {"doc_type_code": 1, "action_code": 3},
            {"doc_type_code": 1, "action_code": 4},
            {"doc_type_code": 1, "action_code": 5},
            {"doc_type_code": 2, "action_code": 1},
            {"doc_type_code": 2, "action_code": 2},
            {"doc_type_code": 2, "action_code": 3},
            {"doc_type_code": 3, "action_code": 1},
            {"doc_type_code": 4, "action_code": 1},
        ]

        actual_type_valid_actions = test_session.query(
            models.DictTypeValidAction,
        ).all()
        assert len(actual_type_valid_actions) == len(
            expected_type_valid_actions,
        )

        for expected_type_valid_action in expected_type_valid_actions:
            actual_type_valid_action = (
                test_session.query(models.DictTypeValidAction)
                .filter_by(
                    doc_type_code=expected_type_valid_action["doc_type_code"],
                    action_code=expected_type_valid_action["action_code"],
                )
                .first()
            )
            assert actual_type_valid_action is not None
            assert (
                actual_type_valid_action.doc_type.code
                == expected_type_valid_action["doc_type_code"]
            )
            assert (
                actual_type_valid_action.action.code
                == expected_type_valid_action["action_code"]
            )

    def test_dict_workflows(self, test_session):
        """Check that dict_workflows table is filled with correct data."""
        expected_workflows = [
            {"code": "FULL", "name": "полная блокировка/разблокировка"},
            {"code": "SUM", "name": "блокировка/разблокировка по сумме"},
            {
                "code": "OPER",
                "name": "блокировка/разблокировка по виду операции (гфд)",
            },
            {
                "code": "UNIT",
                "name": (
                    "блокировка/разблокировка по отдельным балансовым единицам"
                    " (БЕ)"
                ),
            },
            {
                "code": "DOC",
                "name": (
                    "блокировка/разблокировка по номеру документа в указанной"
                    " системе"
                ),
            },
            {"code": "ACC", "name": "блокировка/разблокировка по бух.счету"},
        ]

        actual_workflows = test_session.query(models.DictWorkflow).all()
        assert len(actual_workflows) == len(expected_workflows)

        for expected_workflow in expected_workflows:
            actual_workflow = (
                test_session.query(models.DictWorkflow)
                .filter_by(code=expected_workflow["code"])
                .first()
            )
            assert actual_workflow is not None
            assert actual_workflow.name == expected_workflow["name"]

    def test_dict_operations(self, test_session):
        """Check that dict_operations table is filled with correct data."""
        expected_operations = [
            {
                "sap_code": "P1",
                "sap_name": "ТОВАР",
                "name": "Товарные закупки",
                "blocking": True,
            },
            {
                "sap_code": "P2",
                "sap_name": "НЕТОВАР",
                "name": "Нетоварные закупки",
                "blocking": True,
            },
            {
                "sap_code": "P3",
                "sap_name": "ОПЕРАЦ",
                "name": "Операционные расходы",
                "blocking": True,
            },
            {
                "sap_code": "P4",
                "sap_name": "КАПИТАЛ",
                "name": "Капитальные расходы (CAPEX)",
                "blocking": True,
            },
            {
                "sap_code": "P5",
                "sap_name": "АРЕНДА",
                "name": "Аренда",
                "blocking": True,
            },
            {
                "sap_code": "P6",
                "sap_name": "КОММУНАЛ",
                "name": "Коммунальные платежи",
                "blocking": True,
            },
            {
                "sap_code": "P7",
                "sap_name": "НАЛОГИ",
                "name": "Налоги",
                "blocking": False,
            },
            {
                "sap_code": "P8",
                "sap_name": "ПЕРСОНАЛ",
                "name": "Расчеты с персоналом",
                "blocking": False,
            },
            {
                "sap_code": "P81",
                "sap_name": "ЗАРПЛАТА",
                "name": "Расчеты по зарплате",
                "blocking": False,
            },
            {
                "sap_code": "P82",
                "sap_name": "ИСПЛНЛСТ",
                "name": "Расчеты по исполнительным листам (алименты)",
                "blocking": False,
            },
            {
                "sap_code": "P9",
                "name": "Не товарные закупки ВГО",
                "sap_name": "ВГ НЕТОВАР",
                "blocking": True,
            },
            {
                "sap_code": "P91",
                "name": "Товарные закупки ВГО",
                "sap_name": "ВГ ТОВАР",
                "blocking": True,
            },
            {
                "sap_code": "P99",
                "name": "Переводы внутри БЕ",
                "sap_name": "ВГ ВНТР БЕ",
                "blocking": True,
            },
            {
                "sap_code": "S1",
                "name": "Поступления",
                "sap_name": "ПОСТУПЛ",
                "blocking": True,
            },
            {
                "sap_code": "S2",
                "name": "Поступления ВГО",
                "sap_name": "ВГ ПОСТУПЛ",
                "blocking": True,
            },
        ]

        actual_operations = test_session.query(models.DictOperation).all()
        assert len(actual_operations) == len(expected_operations)

        for expected_operation in expected_operations:
            actual_operation = (
                test_session.query(models.DictOperation)
                .filter_by(sap_code=expected_operation["sap_code"])
                .first()
            )
            assert actual_operation is not None
            assert actual_operation.name == expected_operation["name"]
            assert actual_operation.sap_name == expected_operation["sap_name"]
            assert actual_operation.blocking == expected_operation["blocking"]
