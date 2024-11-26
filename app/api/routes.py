"""
Routes module
"""
from fastapi import APIRouter
from app.api.endpoints.client import client_router

routers = APIRouter()
router_list = [client_router]

for router in router_list:
    routers.include_router(router)
