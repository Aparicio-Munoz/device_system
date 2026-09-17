import logging
from time import perf_counter
from uuid import uuid4

from slowapi import Limiter
from slowapi.util import get_remote_address


logger = logging.getLogger("device_systems.request")
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["120/minute"],
)


async def request_middleware(request, call_next):
    request_id = request.headers.get("X-Request-ID") or uuid4().hex
    request.state.request_id = request_id
    started_at = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        elapsed = perf_counter() - started_at
        logger.exception(
            "%s %s -> 500 in %.4fs request_id=%s",
            request.method,
            request.url.path,
            elapsed,
            request_id,
        )
        raise

    elapsed = perf_counter() - started_at
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"

    logger.info(
        "%s %s -> %s in %.4fs request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
        request_id,
    )
    return response
