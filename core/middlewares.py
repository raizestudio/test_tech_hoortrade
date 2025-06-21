import logging
import time

from django.db import connection, reset_queries

logger = logging.getLogger("query_logger")


class QueryLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reset_queries()
        start = time.time()

        response = self.get_response(request)

        total_time = time.time() - start
        num_queries = len(connection.queries)

        if num_queries > 0:
            logger.debug(f"{request.path} -> {num_queries} queries in {total_time:.2f}s")

        for query in connection.queries:
            logger.debug(query["sql"])

        return response
