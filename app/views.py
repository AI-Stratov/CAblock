"""Module for views."""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import text

import app.models as models
import app.schemas as s
from app.db import get_db
from app.models import Request as AppRequest

router = APIRouter()


@router.post("/block", response_model=s.BlockResponse)
def create_block(request: s.BlockRequest, session=Depends(get_db)):
    """Create block request."""
    data = request.dict()
    details_data = data.pop("details")
    created_at = datetime.now()
    req = AppRequest(**data, blocking=True, created_at=created_at)

    session.add(req)
    session.commit()
    session.refresh(req)

    for detail_data in details_data:
        detail = models.RequestDetail(**detail_data, request_id=req.id)
        session.add(detail)
    session.commit()

    return s.BlockResponse(
        request_id=req.id,
        reg_datetime=req.created_at,
    )


@router.post("/unblock", response_model=s.BlockResponse)
def create_unblock(request: s.BlockRequest, session=Depends(get_db)):
    """Create unblock request."""
    data = request.dict()
    details_data = data.pop("details")
    created_at = datetime.now()

    req = AppRequest(**data, blocking=False, created_at=created_at)

    session.add(req)
    session.commit()
    session.refresh(req)

    for detail_data in details_data:
        detail = models.RequestDetail(**detail_data, request_id=req.id)
        session.add(detail)
    session.commit()

    return s.BlockResponse(
        request_id=req.id,
        reg_datetime=req.created_at,
    )


@router.post("/check", response_model=s.CheckResponse)
def check(request: s.CheckRequest, session=Depends(get_db)):
    """Check request."""
    blocking_status = False

    blocking_query = text(
        """
        SELECT r.* FROM "request" r
        INNER JOIN "request_detail" rd ON r.id = rd.request_id
        WHERE ((r.inn::text = :inn AND :inn != '')
        OR (r.ogrn::text = :ogrn AND :ogrn != '')
        OR (r.sap_num::text = :sap_num AND :sap_num != ''))
        AND rd.workflow_code = 'FULL'
        AND :check_for_dt BETWEEN r.start_at AND r.end_at
        ORDER BY r.created_at DESC
        """,
    )

    blocking_values = {
        "inn": request.inn,
        "ogrn": request.ogrn,
        "sap_num": request.sap_num,
        "check_for_dt": request.check_for_dt,
    }

    blocking_result_proxy = session.execute(blocking_query, blocking_values)
    blocking_data = blocking_result_proxy.fetchall()
    if blocking_data:
        latest_blocking = blocking_data[0]
        blocking_status = latest_blocking.blocking

    if blocking_status:
        doc_query = text(
            """
            SELECT r.* FROM "request" r
            INNER JOIN "request_detail" rd ON r.id = rd.request_id
            WHERE (r.inn = :inn OR r.ogrn = :ogrn OR r.sap_num = :sap_num)
            AND rd.workflow_code = 'DOC'
            AND rd.params ->> 'name_object' = :contract
        """,
        )

        doc_values = {
            "inn": request.inn,
            "ogrn": request.ogrn,
            "sap_num": request.sap_num,
            "contract": request.contract,
        }
        doc_result_proxy = session.execute(doc_query, doc_values)
        doc_data = doc_result_proxy.fetchall()

        if not doc_data:
            blocking_status = True

    return s.CheckResponse(blocking=blocking_status)


@router.get("/dict_operation", response_model=List[s.DictOperation])
def get_dict_operation(session=Depends(get_db)):
    """Get blocking operations."""
    operations = (
        session.query(models.DictOperation).filter_by(blocking=True).all()
    )
    return [
            s.DictOperation(
                sap_code=op.sap_code,
                sap_name=op.sap_name,
                name=op.name
            )
            for op in operations
        ]


@router.get("/dict_system", response_model=List[s.DictSystemSchema])
async def get_dict_system(session=Depends(get_db)):
    """Get blocking systems."""
    systems = session.query(models.DictSystem).filter_by(source_doc=True).all()
    return [
        s.DictSystemSchema(
            code=system.code,
            name=system.name,
        )
        for system in systems
    ]


@router.get("/dict_doc_type", response_model=List[s.DictDocTypeSchema])
def get_dict_doc_type(system_code: int, session=Depends(get_db)):
    """Get blocking document types."""
    doc_types = (
        session.query(models.DictDocType)
        .join(models.DictSystem)
        .filter(
            models.DictSystem.code == system_code,
            models.DictSystem.source_doc,
        )
        .all()
    )
    return [
        s.DictDocTypeSchema(
            code=doc_type.code,
            name=doc_type.name,
            fullname=doc_type.fullname,
        )
        for doc_type in doc_types
    ]


@router.get("/dict_action", response_model=List[s.DictActionCodeSchema])
def get_dict_action(doc_type_code: int, session=Depends(get_db)):
    """Get blocking actions."""
    actions = (
        session.query(models.DictAction.code, models.DictAction.name)
        .join(
            models.DictTypeValidAction,
            models.DictTypeValidAction.action_code == models.DictAction.code,
        )
        .join(
            models.DictDocType,
            models.DictDocType.code
            == models.DictTypeValidAction.doc_type_code,
        )
        .filter(models.DictDocType.code == doc_type_code)
        .all()
    )
    return [
        s.DictActionCodeSchema(
            code=action.code,
            name=action.name,
        )
        for action in actions
    ]


@router.post("/report")
def create_report():
    """TODO: Create report."""
    pass
