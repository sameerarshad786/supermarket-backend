def filtered_paginated_response(self, queryset):
    queryset = self.filter_queryset(self.queryset)
    page = self.paginate_queryset(queryset)
    serializer = self.serializer_class(
        page, context={"request": self.request}, many=True
    )
    data = self.get_paginated_response(serializer.data).data
    return data
