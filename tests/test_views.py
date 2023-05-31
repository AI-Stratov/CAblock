"""Class for testing views of the application."""
from http import HTTPStatus


class TestViews:
    """Class for testing views of the application."""

    params = {
        "is_resident": False,
        "inn": "testinn",
        "ogrn": "testogrn",
        "in_sap": True,
        "sap_num": "testsapnum",
        "mdm_id": "testmdmid",
        "from_system": 0,
        "created_by": "testuser",
        "approved_at": "2021-01-01T00:00:00",
        "approved_by": "testadmin",
        "start_at": "2010-01-01T00:00:00",
        "end_at": "2023-12-31T23:59:59",
        "description": "desc",
        "details": [
            {
                "workflow_code": "FULL",
                "params": {
                    "max_sum": 0,
                    "operation_sap_code": ["string"],
                    "balance_unit": "",
                    "system_code": 0,
                    "doc_type_code": 0,
                    "action_code": 0,
                    "doc_num": "",
                    "name_object": "",
                    "contract": "",
                    "debit": True,
                    "account": "",
                },
            },
        ],
    }
    check_params = {
        "from_system": 0,
        "employee": "",
        "inn": "testinn",
        "ogrn": "testogrn",
        "sap_num": "testsapnum",
        "contract": "",
        "check_for_dt": "2023-05-26T16:59:25.617Z",
    }

    def test_smoke(self, test_client):
        """Check if app is running."""
        response = test_client.get("/")
        assert response.status_code == HTTPStatus.OK

    def test_block(self, test_client):
        """Request with proper params should return 200 and request_id."""
        response = test_client.post("/block", json=self.params)
        reg_datetime = response.json().get("reg_datetime")
        expected_response = {"request_id": 1, "reg_datetime": reg_datetime}

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_response

    def test_block_bad_request(self, test_client):
        """Request with bad params should return 422."""
        self.params["inn"] = ""
        self.params["ogrn"] = ""
        self.params["sap_num"] = ""
        response = test_client.post("/block", json=self.params)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_unblock(self, test_client):
        """Request with proper params should return 200 and request_id."""
        self.params["inn"] = "unblockinn"
        self.params["ogrn"] = "unblockogrn"
        self.params["sap_num"] = "unblocksapnum"
        response = test_client.post("/unblock", json=self.params)
        reg_datetime = response.json().get("reg_datetime")
        expected_response = {"request_id": 2, "reg_datetime": reg_datetime}
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == expected_response

    def test_check_true(self, test_client):
        """Check request should return 200 and blocking: True."""
        expected_response = {
                "blocking": True,
            }
        response = test_client.post("/check", json=self.check_params)
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == expected_response

    def test_check_false(self, test_client):
        """Check request should return 200 and blocking: False."""
        self.check_params["inn"] = "checkfalseinn"
        self.check_params["ogrn"] = "checkfalseogrn"
        self.check_params["sap_num"] = "checkfalsesapnum"
        expected_response = {
                "blocking": False,
            }
        response = test_client.post("/check", json=self.check_params)
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == expected_response

    def test_dict_operation(self, test_client):
        """Request should return 200 and dict_operation."""
        response = test_client.get("/dict_operation")
        expected_response = [
                {
                    "sap_code": "P1",
                    "sap_name": "ТОВАР",
                    "name": "Товарные закупки",
                },
                {
                    "sap_code": "P2",
                    "sap_name": "НЕТОВАР",
                    "name": "Нетоварные закупки",
                },
                {
                    "sap_code": "P3",
                    "sap_name": "ОПЕРАЦ",
                    "name": "Операционные расходы",
                },
                {
                    "sap_code": "P4",
                    "sap_name": "КАПИТАЛ",
                    "name": "Капитальные расходы (CAPEX)",
                },
                {"sap_code": "P5", "sap_name": "АРЕНДА", "name": "Аренда"},
                {
                    "sap_code": "P6",
                    "sap_name": "КОММУНАЛ",
                    "name": "Коммунальные платежи",
                },
                {
                    "sap_code": "P9",
                    "sap_name": "ВГ НЕТОВАР",
                    "name": "Не товарные закупки ВГО",
                },
                {
                    "sap_code": "P91",
                    "sap_name": "ВГ ТОВАР",
                    "name": "Товарные закупки ВГО",
                },
                {
                    "sap_code": "P99",
                    "sap_name": "ВГ ВНТР БЕ",
                    "name": "Переводы внутри БЕ",
                },
                {
                    "sap_code": "S1",
                    "sap_name": "ПОСТУПЛ",
                    "name": "Поступления",
                },
                {
                    "sap_code": "S2",
                    "sap_name": "ВГ ПОСТУПЛ",
                    "name": "Поступления ВГО",
                },
                {
                    "sap_code": "S3",
                    "sap_name": "test_system",
                    "name": "test_name",
                },
            ]
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == expected_response

    def test_dict_system(self, test_client):
        """Request should return 200 and dict_system."""
        response = test_client.get("/dict_system")
        expected_response = [
                {"code": 1, "name": "SAP ERP"},
                {"code": 2, "name": "СЭД"},
            ]
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == expected_response

    def test_dict_doc_type(self, test_client):
        """Request should return 200 and dict_doc_type."""
        response = test_client.get("/dict_doc_type", params={"system_code": 1})
        expected_response = [
                {
                    "code": 1,
                    "name": "FI",
                    "fullname": "бухгалтерский документ",
                },
                {"code": 2, "name": "MM", "fullname": "заказ на закупку"},
            ]
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == expected_response

    def test_dict_action(self, test_client):
        """Request should return 200 and dict_action."""
        response = test_client.get("/dict_action", params={"doc_type_code": 2})
        expected_response = [
                {"code": 1, "name": "изменение"},
                {"code": 2, "name": "сторнирование"},
                {"code": 3, "name": "создать последующий"},
            ]
        assert response.status_code == HTTPStatus.OK, response.text
        assert response.json() == expected_response
