ZENDESK_API_ENDPOINTS = {
    "/api/v2/help_center/articles": {
        "response_name": "articles",
        "pagination": {
            "type": "page_number",  # Assume this uses traditional page number pagination
            "param_name": "page",   # The query parameter name used for specifying the page number
            "size_param": "per_page",  # Parameter name for specifying number of items per page
            "size": 100  # Number of items per page
        }
    },
    "/api/v2/guide/content_tags": {
        "response_name": "content_tags",
        "pagination": {
            "type": "cursor",
            "param_name": "after_cursor",  # The query parameter name used for specifying the cursor
            "meta_key": "meta",  # Key in the response where pagination metadata is found
            "has_more": "has_more",  # Key in the meta object indicating more data is available
            "cursor_key": "after_cursor"  # Key in the meta object for the next cursor
        }
    }
}
