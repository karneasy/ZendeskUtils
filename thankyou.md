{% for comment in ticket.public_comments offset:0 limit:1 %}
{% assign sanitized_comment = comment.value | replace: '\r\n', ' ' | replace: '\n', ' ' | replace: '\r', ' ' %}
{% if sanitized_comment.size < 25 %}
{
  "status": "solved",
  "additional_tags": ["thankyou"]
}
{% endif %}
{% endfor %}
