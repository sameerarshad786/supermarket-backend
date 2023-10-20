from django.conf import settings

from elasticsearch import Elasticsearch


def elastic_search_client():
    return Elasticsearch(
        hosts=settings.ELASTIC_SEARCH_HOST,
        verify_certs=False,
        ssl_show_warn=False,
        http_auth=(
            settings.ELASTIC_SEARCH_USER,
            settings.ELASTIC_SEARCH_PASSWORD
        )
    )
