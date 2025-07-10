# backend/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import OptionData, SessionLocal, Base, engine
from nse_utils import get_option_chain_data
from sqlalchemy.future import select
from sqlalchemy import desc
import asyncio

app = FastAPI()


# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/fetch-and-save")
async def fetch_and_save(db: AsyncSession = Depends(get_db)):
    records = get_option_chain_data()

    # Filter only strike data with both CE & PE
    option_list = [item for item in records if "CE" in item and "PE" in item]

    # Sort by Call OI descending
    top_6 = sorted(option_list, key=lambda x: x["CE"]["openInterest"], reverse=True)[:6]

    # Save each to DB
    for item in top_6:
        ce = item["CE"]
        pe = item["PE"]
        entry = OptionData(
            strike_price=ce["strikePrice"],
            call_oi=ce["openInterest"],
            call_oi_change=ce["changeinOpenInterest"],
            call_volume=ce["totalTradedVolume"],
            put_oi=pe["openInterest"],
            put_oi_change=pe["changeinOpenInterest"],
            put_volume=pe["totalTradedVolume"]
        )
        db.add(entry)
    await db.commit()
    return {"status": "✅ Data saved"}


@app.get("/latest-data")
async def get_latest_data(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(OptionData).order_by(desc(OptionData.timestamp)).limit(6))
    data = result.scalars().all()
    return [d.__dict__ for d in data]
