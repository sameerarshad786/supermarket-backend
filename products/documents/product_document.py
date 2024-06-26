
from django.conf import settings

from elasticsearch_dsl import Text, Search, Q, Date, Keyword, AttrList, Object
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.document import Document

from ..utils import elastic_search_client
from .document_fields import RangeField


connections.create_connection(
    hosts=settings.ELASTIC_SEARCH_HOST,
    verify_certs=False,
    ssl_show_warn=False,
    http_auth=(
        settings.ELASTIC_SEARCH_USER,
        settings.ELASTIC_SEARCH_PASSWORD
    )
)


class ProductDocument(Document):
    index = "products"

    id = Text()
    name = Text()
    images = AttrList(l=[])
    price = RangeField()
    brand = Object()
    category = Object()
    condition = Keyword()
    by = Keyword()
    url = Text()
    created_at = Date()
    updated_at = Date()

    @classmethod
    def search_product_using_es(
        cls, search, condition, category, brand, by, price, page, page_size
    ) -> list:
        client = elastic_search_client()
        es = Search(
            using=client, index=cls.index
        ).sort({"created_at": "desc", "updated_at": "desc"})
        should = []
        if search:
            should.extend(
                [Q("match", name=search), Q("match", description=search)]
            )
        if condition:
            should.append(Q("term", condition=condition))
        if category:
            should.append(Q("match", category__sub_category=category))
        if brand:
            should.append(Q("term", brand__name=brand))
        if by:
            should.append(Q("term", by=by))

        es = es.query("bool", should=should)
        if price:
            if "," in price:
                price = price.split(",")
                price_filter = {
                    "gt": float(price[0]),
                    "lt": float(price[1])
                }
            else:
                price_filter = {
                    "lt": float(price)
                }
            es = es.query(
                "bool",
                should=[
                    Q(
                        "range",
                        price=price_filter
                    )
                ]
            ).sort({"price": "asc"})

        es = es.extra(from_=page, size=page_size)

        response = es.execute()
        return response

    @classmethod
    def build_index(cls):
        client = elastic_search_client()
        index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "price": {"type": "float_range"},
                    "condition": {"type": "keyword"},
                    "by": {"type": "keyword"},
                    "brand": {"type": "object"},
                    "category": {"type": "object"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            }
        }
        client.indices.create(index=cls.index, body=index_settings)

    @classmethod
    def drop_index(cls):
        client = elastic_search_client()
        client.indices.delete(index=cls.index)
