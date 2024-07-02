# rate_limiter.py
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter

class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

def configure_cached_limiter_session(max_requests, duration, cache_file):
    limiter = Limiter(RequestRate(max_requests, Duration.SECOND * duration))
    bucket_class = MemoryQueueBucket
    backend = SQLiteCache(cache_file)

    session = CachedLimiterSession(
        limiter=limiter,
        bucket_class=bucket_class,
        backend=backend,
    )

    return session