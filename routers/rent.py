from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

import models
from validation import RentRequestBase
from database import db_dependency
from internal.admin import rented_days

router = APIRouter(
    prefix='/rent', 
    tags=['user_house_rent']
)


# this endpoint adds request for rent in database
@router.post("/rent_house", status_code=status.HTTP_201_CREATED)
async def rent_house(rent_req: RentRequestBase, db: db_dependency):
    """
    This endpoint adds rent request to `rent_request` table
    """

    all_rents = await rented_days(db)
    rent_day_start_forbidden: bool = rent_req.wished_date_start in all_rents
    rent_day_end_forbidden:   bool = rent_req.wished_date_end in all_rents

    if rent_day_start_forbidden or rent_day_end_forbidden:
        raise HTTPException(
            status_code=409, detail="the house is rented by another person"
        )
    else:
        db_request_rent = models.RentRequest(**rent_req.model_dump())
        db.add(db_request_rent)
        await db.commit()


@router.get("/get_rent", status_code=status.HTTP_201_CREATED)
async def get_rents(db: db_dependency):
    cons = await db.execute(select(models.RentRequest))
    return cons.scalars().all()
