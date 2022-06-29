from fastapi import APIRouter
from schemas.flower import flowersEntity
from config.mongodb import conn

flower = APIRouter()

@flower.get('/')
async def list_all_flowers():
    print(conn.hanlhn.flowers.find())
    print(flowersEntity(conn.hanlhn.flowers.find()))
    return flowersEntity(conn.hanlhn.flowers.find())



