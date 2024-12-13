ZENDESK_API_ENDPOINTS = {
    "?include=usage_1h,usage_24h,usage_7d,usage_30d&page[size]=100": {
        "response_name": "macros_usage",
        "pagination": {
            "type": "cursor",  # Assuming cursor pagination for this endpoint
            "param_name": "page",  # Cursor parameter name (if applicable)
            "meta_key": "meta",  # Key in the response containing metadata
            "cursor_key": "next_cursor",  # Key in metadata for the cursor
            "has_more": "has_more"  # Key in metadata to check if more data exists
        }
    }
}
