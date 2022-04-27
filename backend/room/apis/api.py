# import datetime
# import logging
#
# from django.http import Http404
# from django.shortcuts import get_object_or_404
# from ninja import Router
#
#
# router = Router(tags=['Group - Main'])
# logger = logging.getLogger('room')
#
#
# @router.post("/", response={200: PostSuccess, 500: ErrorMessage})
# def create_group(request, payload: GroupSchemaIn):
#     try:
#         group = Group.objects.create(**payload.dict())
#         return 200, {"id": group.id}
#     except Exception as e:
#         logger.error(e.__str__())
#         return 500, server_error_return
#
#
# @router.get("/{group_id}", response={200: GroupSchemaOut, 404: ErrorMessage, 500: ErrorMessage})
# def get_group(request, group_id: str):
#     try:
#         group = get_object_or_404(Group, id=group_id, is_deleted=False)
#         return 200, group
#
#     except Http404:
#         return 404, not_found_error_return
#
#     except Exception as e:
#         logger.error(e.__str__())
#         return 500, server_error_return
#
#
# @router.put("/{group_id}", response={200: PostSuccess, 404: ErrorMessage, 500: ErrorMessage})
# def update_group(request, group_id: str, payload: PutGroupSchemaIn):
#     try:
#         group = get_object_or_404(Group, id=group_id)
#         for attr, value in payload.dict().items():
#             setattr(group, attr, value)
#         group.save()
#         return 200, {"id": group.id}
#
#     except Http404:
#         return 404, not_found_error_return
#
#     except Exception as e:
#         logger.error(e.__str__())
#         return 500, server_error_return
#
#
# @router.delete("/{group_id}", response={200: SuccessStatus, 404: ErrorMessage, 500: ErrorMessage})
# def delete_group(request, group_id: str):
#     try:
#         group = get_object_or_404(Group, id=group_id)
#         group.is_deleted = True
#         group.deleted_time = datetime.datetime.now()
#         group.save()
#         return 200, {"success": True}
#
#     except Http404:
#         return 404, not_found_error_return
#
#     except Exception as e:
#         logger.error(e.__str__())
#         return 500, server_error_return
