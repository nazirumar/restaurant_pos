import logging
from django_tenants.utils import get_tenant_model

logger = logging.getLogger(__name__)

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant = None
        try:
            if request.user.is_authenticated and hasattr(request.user, "tenant"):
                # Get tenant directly from user relation
                request.tenant = request.user.tenant
                logger.debug(f"Tenant set from authenticated user: {request.tenant}")
            else:
                # Fallback to subdomain lookup
                host = request.get_host().lower()
                subdomain = host.split(".")[0]

                try:
                    tenant = get_tenant_model().objects.get(subdomain=subdomain)
                    request.tenant = tenant
                    logger.debug(f"Tenant set from subdomain: {request.tenant}")
                except get_tenant_model().DoesNotExist:
                    request.tenant = None
                    logger.warning(f"No tenant found for subdomain: {subdomain}")

                    # Optional: fallback to default tenant
                    try:
                        request.tenant = get_tenant_model().objects.get(subdomain="default")
                        logger.debug(f"Fallback to default tenant: {request.tenant}")
                    except get_tenant_model().DoesNotExist:
                        logger.warning("No default tenant found")
                        request.tenant = None
        except Exception as e:
            logger.error(f"Error in TenantMiddleware: {str(e)}")
            request.tenant = None

        return self.get_response(request)
