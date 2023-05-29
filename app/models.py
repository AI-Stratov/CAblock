"""Models for database tables."""
import json
from datetime import datetime

from sqlalchemy import (TIMESTAMP, BigInteger, Boolean, Column, ForeignKey,
                        SmallInteger, String, Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db import Base


class Request(Base):
    """Request model."""

    __tablename__ = "request"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    is_resident = Column(
        Boolean,
        nullable=False,
    )
    inn = Column(
        String(60),
        nullable=True,
    )
    ogrn = Column(
        String(60),
        nullable=True,
    )
    in_sap = Column(
        Boolean,
        nullable=False,
        default=False,
    )
    sap_num = Column(
        String(20),
        nullable=True,
        default=None,
    )
    mdm_id = Column(
        String(20),
        nullable=True,
    )
    blocking = Column(
        Boolean,
        nullable=False,
    )
    from_system = Column(
        SmallInteger,
        ForeignKey("dict_system.code"),
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP,
        nullable=False,
    )
    created_by = Column(
        String(30),
        nullable=False,
    )
    approved_at = Column(
        TIMESTAMP,
        nullable=True,
    )
    approved_by = Column(
        String(30),
        nullable=True,
    )
    start_at = Column(
        TIMESTAMP,
        default=datetime(1990, 1, 1, 0, 0, 0),
        nullable=False,
    )
    end_at = Column(
        TIMESTAMP,
        default=datetime(9999, 12, 31, 23, 59, 59),
        nullable=False,
    )
    description = Column(
        Text,
        nullable=True,
    )

    details = relationship("RequestDetail", back_populates="request")
    system = relationship("DictSystem")


class DictAction(Base):
    """Dictionary of actions model."""

    __tablename__ = "dict_action"

    code = Column(
        SmallInteger,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(20),
        nullable=False,
    )


class DictDocType(Base):
    """Dictionary of document types model."""

    __tablename__ = "dict_doc_type"

    code = Column(
        SmallInteger,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(20),
        nullable=False,
    )
    fullname = Column(
        String(50),
    )
    system_code = Column(
        SmallInteger,
        ForeignKey("dict_system.code"),
        nullable=False,
    )

    system = relationship("DictSystem")


class DictOperation(Base):
    """Dictionary of operations model."""

    __tablename__ = "dict_operation"

    sap_code = Column(
        String(4),
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    sap_name = Column(
        String(15),
        nullable=True,
    )
    name = Column(
        String(75),
        nullable=False,
    )
    blocking = Column(
        Boolean,
        nullable=False,
    )


class DictSystem(Base):
    """Dictionary of systems model."""

    __tablename__ = "dict_system"

    code = Column(
        SmallInteger,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(20),
        nullable=False,
    )
    can_block = Column(
        Boolean,
        default=False,
    )
    source_doc = Column(
        Boolean,
        default=False,
    )


class DictTypeValidAction(Base):
    """Dictionary of valid actions for document types model."""

    __tablename__ = "dict_type_valid_action"

    doc_type_code = Column(
        SmallInteger,
        ForeignKey("dict_doc_type.code"),
        nullable=False,
        primary_key=True,
    )
    action_code = Column(
        SmallInteger,
        ForeignKey("dict_action.code"),
        nullable=False,
        primary_key=True,
    )

    doc_type = relationship("DictDocType")
    action = relationship("DictAction")


class DictWorkflow(Base):
    """Dictionary of workflows model."""

    __tablename__ = "dict_workflow"

    code = Column(
        String(5),
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(100),
        nullable=False,
    )


class RequestDetail(Base):
    """Request detail model."""

    __tablename__ = "request_detail"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    request_id = Column(
        BigInteger,
        ForeignKey("request.id"),
        nullable=False,
    )
    workflow_code = Column(
        String,
        ForeignKey("dict_workflow.code"),
        nullable=False,
    )
    params = Column(
        JSONB,
        nullable=True,
    )

    request = relationship("Request", back_populates="details")
    workflow = relationship("DictWorkflow")
