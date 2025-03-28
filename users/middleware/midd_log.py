import logging
import time
from django.http import JsonResponse
from django.utils.timezone import now
from users.models import Profile
from users.models import UserRole


logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        request_data = {
            'method': request.method,
            'ip_address': self.get_client_ip(request),
            'path': request.path,
        }
        logger.info(request_data)
        response = self.get_response(request)
        duration = time.time() - start_time
        request_dict = {
            'status_code': response.status_code,
            'duration': duration,
        }
        logger.info(request_dict)
        return response

    def get_client_ip(self, request):
        """Extract the real IP address of the user."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.block_time = 60  # Cooldown period in seconds
        self.role_limits = {
            UserRole.GOLD: 10,
            UserRole.SILVER: 5,
            UserRole.BRONZE: 2,
            UserRole.NORMAL: 1,  # For unauthenticated users
        }
        self.limited_paths = ["/profile/"]

    def __call__(self, request):
        if request.path in self.limited_paths:
            return self.handle_authenticated(request)
        return self.get_response(request)

    def handle_authenticated(self, request):
        profile = self.get_user_profile(request)
        role = UserRole(profile.status)
        max_requests = self.role_limits.get(role, 1)

        if not profile.last_hit:
            profile.last_hit = now()
            profile.count = 1
            profile.save()
            return self.get_response(request)

        time_diff = (now() - profile.last_hit).total_seconds()

        if time_diff < self.block_time:
            print("count1", profile.count)
            if profile.count >= max_requests:
                print("count", profile.count)
                return JsonResponse({"error": "You are blocked"}, status=429)
            profile.count += 1
        else:
            profile.count = 1
            profile.last_hit = now()

        profile.save()
        return self.get_response(request)

    def get_user_profile(self, request):
        try:
            return request.user.profile
        except Profile.DoesNotExist:
            return None
