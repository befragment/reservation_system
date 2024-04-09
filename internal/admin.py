from datetime import date, datetime, timezone

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, delete

from utils.dateworker import DateWorker
from validation import ContractBase
import models
from database import db_dependency


router = APIRouter(
    prefix='/admin',
    tags=['admin_panel']
)

dWorker = DateWorker()


@router.delete("/delete_contract/{contract_id_to_delete}")
async def delete_contract(contract_id_to_delete: int, db: db_dependency):
    """
    Delete contract by its id
    """
    await db.execute(
        delete(models.Contract).where(
            models.Contract.contract_id == contract_id_to_delete
        )
    )
    await db.commit()


@router.get("/get_contracts")
async def get_contracts(db: db_dependency):
    """
    Return the whole `contract` table in json format
    """
    cons = await db.execute(select(models.Contract))
    return cons.scalars().all()


@router.post("/set_contract", status_code=status.HTTP_201_CREATED)
async def set_contract(contract: ContractBase, db: db_dependency):
    """
    Adding a contract to `contract` table after actual agreement with client
    """

    all_rents: list[date] = await rented_days(db)
    contract_day_start_rented: bool = contract.datetime_start.date() in all_rents
    contract_day_end_rented:   bool = contract.datetime_end.date() in all_rents

    if contract_day_start_rented or contract_day_end_rented:
        raise HTTPException(
            status_code=409, detail="the house is rented by another person"
        )
    else:
        db_contract = models.Contract(**contract.model_dump())
        db.add(db_contract)
        await db.commit()


@router.get("/get_contracts/rented_dates")
async def rented_days(db: db_dependency) -> list:
    """
    Return the list of dates from `contract` table in which the house is rented
    """
    
    rented_dates = list()
    contracts = await get_contracts(db)

    for contract_interval in contracts:
        rented_intervals: list[tuple[datetime, datetime]] = list(
            (contract_interval.datetime_start, contract_interval.datetime_end)
        )
        start_day: date = rented_intervals[0].date()
        end_day: date = rented_intervals[1].replace(tzinfo=None).date()
        today: date = datetime.now(timezone.utc).replace(tzinfo=None).date()
        if today > end_day:
            continue
        else:
            dates_between = await dWorker.get_dates_between(start_day, end_day)
            rented_dates.extend(dates_between)


    return tuple(
        datetime.strptime(date_string, '%Y-%m-%d').date() 
        for date_string in rented_dates
    )
