from ninja import NinjaAPI

from room.apis.room_api import router as room_router
from account.apis.account_api import router as account_router

api = NinjaAPI(version='2.0.0', title="CTUDY API", description="Ctudy Backend RESTful API", csrf=True)

# User
api.add_router('/account/', account_router)

# Room
api.add_router('/study/room/', room_router)
