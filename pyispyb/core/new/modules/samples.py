from typing import Optional, Any
from flask import request
import sqlalchemy
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql.expression import func, distinct

from pyispyb.app.extensions import db
from ....core import models
from ..database.utils import Paged, page, with_metadata


def with_auth_to_session(query: "sqlalchemy.orm.Query[Any]", column: "sqlalchemy.Column[Any]"):
    """Join relevant tables to authorise right through to SessionHasPerson

    in case of not being admin, can be reused"""
    return (
        query.join(models.Proposal, column == models.Proposal.proposalId)
        .join(
            models.BLSession, models.BLSession.proposalId == models.Proposal.proposalId
        )
        .join(
            models.SessionHasPerson,
            models.BLSession.sessionId == models.SessionHasPerson.sessionId,
        )
        .filter(models.SessionHasPerson.personId == request.person.personId)
    )


def get_samples(
    skip: int,
    limit: int,
    blSampleId: Optional[int] = None,
    proteinId: Optional[int] = None,
    admin: Optional[bool] = False,
) -> Paged[models.BLSample]:
    metadata = {
        "subsamples": func.count(distinct(models.BLSubSample.blSubSampleId)),
        "datacollections": func.count(distinct(models.DataCollection.dataCollectionId)),
    }

    query = (
        db.session.query(models.BLSample, *metadata.values())
        .join(models.BLSample.Crystal)
        .options(
            contains_eager(models.BLSample.Crystal).load_only(
                models.Crystal.cell_a,
                models.Crystal.cell_b,
                models.Crystal.cell_c,
                models.Crystal.cell_alpha,
                models.Crystal.cell_beta,
                models.Crystal.cell_gamma,
            )
        )
        .join(models.Crystal.Protein)
        .options(
            contains_eager("Crystal.Protein").load_only("name", "acronym"),
        )
        .outerjoin(
            models.BLSubSample,
            models.BLSubSample.blSampleId == models.BLSample.blSampleId,
        )
        .outerjoin(
            models.DataCollectionGroup,
            models.DataCollectionGroup.blSampleId == models.BLSample.blSampleId,
        )
        .outerjoin(
            models.DataCollection,
            models.DataCollectionGroup.dataCollectionGroupId
            == models.DataCollection.dataCollectionGroupId,
        )
        .group_by(models.BLSample.blSampleId)
    )

    if not admin:
        query = (
            query.join(
                models.Container,
                models.BLSample.containerId == models.Container.containerId,
            )
            .join(models.Dewar, models.Container.dewarId == models.Dewar.dewarId)
            .join(
                models.Shipping, models.Dewar.shippingId == models.Shipping.shippingId
            )
        )
        query = with_auth_to_session(query, models.Shipping.proposalId)

    if blSampleId:
        query = query.filter(models.BLSample.blSampleId == blSampleId)

    if proteinId:
        query = query.filter(models.Protein.proteinId == proteinId)

    total = query.count()
    query = page(query, skip=skip, limit=limit)
    results = with_metadata(query.all(), list(metadata.keys()))

    return Paged(total=total, results=results, skip=skip, limit=limit)