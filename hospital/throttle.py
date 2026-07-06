# from django_ratelimit.decorators import ratelimit
# from django_ratelimit.exceptions import Ratelimited
# from django.http import JsonResponse


# def ratelimited_response(request, exception):
#     """Handler 429 avec header Retry-After (RFC 6585)."""
#     return JsonResponse(
#         {"error": "Trop de requêtes. Réessayez dans un moment."},
#         status=429,
#         headers={"Retry-After": "60"},
#     )