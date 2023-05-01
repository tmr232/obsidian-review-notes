
[[{{ prev_week }}|Prev]] | [[{{ next_week}}|Next]]

| Sun | Mon | Tue | Wed | Thu | Fri | Sat |
|-----|-----|-----|-----|-----|-----|-----|
| {% for day in weekdays %} [[{{day}}]] |{% endfor %}

{% for link in links|sort %}
- {{ link }}
{%- endfor %}