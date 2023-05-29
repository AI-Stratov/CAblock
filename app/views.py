"""Module for views."""
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text

import app.models as models
import app.schemas as schemas
from app.db import get_db
from app.models import Request as AppRequest

router = APIRouter()


@router.post("/block", response_model=schemas.BlockResponse)
def create_block(request: schemas.BlockRequest, session=Depends(get_db)):
    """Create block request."""
    details_data = request.details
    created_at = datetime.now()

    req = AppRequest(
        is_resident=request.is_resident,
        inn=request.inn,
        ogrn=request.ogrn,
        in_sap=request.in_sap,
        sap_num=request.sap_num,
        mdm_id=request.mdm_id,
        blocking=True,
        from_system=request.from_system,
        created_at=created_at,
        created_by=request.created_by,
        approved_at=request.approved_at,
        approved_by=request.approved_by,
        start_at=request.start_at,
        end_at=request.end_at,
        description=request.description,
    )

    session.add(req)
    session.commit()
    session.refresh(req)

    detail_data = details_data[0]
    params_json = jsonable_encoder(detail_data.params)
    detail = models.RequestDetail(
        workflow_code=detail_data.workflow_code,
        params=params_json,
        request_id=req.id,
    )
    session.add(detail)
    session.commit()

    return schemas.BlockResponse(
        request_id=req.id,
        reg_datetime=req.created_at,
    )


@router.post("/unblock", response_model=schemas.BlockResponse)
def create_unblock(request: schemas.BlockRequest, session=Depends(get_db)):
    """Create unblock request."""
    details_data = request.details
    created_at = datetime.now()

    req = AppRequest(
        is_resident=request.is_resident,
        inn=request.inn,
        ogrn=request.ogrn,
        in_sap=request.in_sap,
        sap_num=request.sap_num,
        mdm_id=request.mdm_id,
        blocking=False,
        from_system=request.from_system,
        created_at=created_at,
        created_by=request.created_by,
        approved_at=request.approved_at,
        approved_by=request.approved_by,
        start_at=request.start_at,
        end_at=request.end_at,
        description=request.description,
    )

    session.add(req)
    session.commit()
    session.refresh(req)

    detail_data = details_data[0]
    params_json = jsonable_encoder(detail_data.params)
    detail = models.RequestDetail(
        workflow_code=detail_data.workflow_code,
        params=params_json,
        request_id=req.id,
    )
    session.add(detail)
    session.commit()

    return schemas.BlockResponse(
        request_id=req.id,
        reg_datetime=req.created_at,
    )


@router.post("/check", response_model=schemas.CheckResponse)
def check(request: schemas.CheckRequest, session=Depends(get_db)):
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

    return schemas.CheckResponse(blocking=blocking_status)


@router.get("/dict_operation", response_model=schemas.DictOperationResponse)
def get_dict_operation(session=Depends(get_db)):
    """Get blocking operations."""
    operations = (
        session.query(models.DictOperation).filter_by(blocking=True).all()
    )
    data = [
        {
            "sap_code": op.sap_code,
            "sap_name": op.sap_name,
            "name": op.name,
        }
        for op in operations
    ]
    return schemas.DictOperationResponse(data=data)


@router.get("/dict_system", response_model=schemas.DictSystemResponse)
async def get_dict_system(session=Depends(get_db)):
    """Get blocking systems."""
    systems = session.query(models.DictSystem).filter_by(source_doc=True).all()
    data = [{"code": system.code, "name": system.name} for system in systems]
    return schemas.DictSystemResponse(data=data)


@router.get("/dict_doc_type", response_model=schemas.DictDocTypeResponse)
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
    data = [
        {
            "code": doc_type.code,
            "name": doc_type.name,
            "fullname": doc_type.fullname,
        }
        for doc_type in doc_types
    ]
    return schemas.DictDocTypeResponse(data=data)


@router.get("/dict_action", response_model=schemas.DictActionResponse)
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
    data = [
        {
            "code": action.code,
            "name": action.name,
        }
        for action in actions
    ]
    return schemas.DictActionResponse(data=data)


@router.post("/report")
def create_report():
    """TODO: Create report."""
    pass
