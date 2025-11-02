from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')
    if not properties:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, 3600)
    return properties

def get_redis_cache_metrics():
    redis_conn = get_redis_connection("default")
    info = redis_conn.info()

    keyspace_hits = info.get("keyspace_hits", 0)
    keyspace_misses = info.get("keyspace_misses", 0)
    total_requests = keyspace_hits + keyspace_misses

    hit_ratio = (keyspace_hits / total_requests) if total_requests > 0 else 0

    metrics = {
        "keyspace_hits": keyspace_hits,
        "keyspace_misses": keyspace_misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics

