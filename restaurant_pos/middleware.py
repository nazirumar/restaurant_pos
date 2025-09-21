import logging
from django.http import Http404
from tenants.models import Tenant

logger = logging.getLogger(__name__)

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None
        try:
            if request.user.is_authenticated:
                request.tenant = request.user.tenant
                logger.debug(f"Tenant set from authenticated user: {request.tenant}")
            else:
                host = request.get_host().lower()
                subdomain = host.split('.')[0]
                try:
                    request.tenant = Tenant.objects.get(subdomain=subdomain)
                    logger.debug(f"Tenant set from subdomain: {request.tenant}")
                except Tenant.DoesNotExist:
                    logger.warning(f"No tenant found for subdomain: {subdomain}")
                    # Fallback to default tenant if it exists
                    try:
                        request.tenant = Tenant.objects.get(subdomain='default')
                        logger.debug(f"Fallback to default tenant: {request.tenant}")
                    except Tenant.DoesNotExist:
                        logger.warning("No default tenant found")
                        request.tenant = None
        except Exception as e:
            logger.error(f"Error in TenantMiddleware: {str(e)}")
            request.tenant = None
        return self.get_response(request)