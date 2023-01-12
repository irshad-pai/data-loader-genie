{% macro get_sdm_partition_clause() %}
    days(event_timestamp_ts),days(parsed_interval_timestamp_ts)
{% endmacro %}

{% macro get_ps_sdm_hidden_partition_columns() %}
event_timestamp_ts,parsed_interval_timestamp_ts
{% endmacro %}

{% macro get_ps_sdm_hidden_partition_clause() %}
    days(event_timestamp_ts),days(parsed_interval_timestamp_ts)
{% endmacro %}