from ninja import NinjaAPI

from room.apis.room_api import router as room_router
from room.apis.member_api import router as member_router
from account.apis.account_api import router as account_router
from coupon.apis.coupon_api import router as coupon_router
from utils.error import CtudyException

api = NinjaAPI(version='2.0.0', title="CTUDY API", description="Ctudy Backend RESTful API", csrf=False)


@api.exception_handler(CtudyException)
def ctudy_exception(request, exc):
    return api.create_response(request, exc.message, status=exc.code)


# User
api.add_router('/account/', account_router)

# Room
api.add_router('/study/room/', room_router)
api.add_router('/study/room/member/', member_router)

# Coupon
api.add_router('/coupon/', coupon_router)
