{% macro incremental_filter_clause() %} 
    parsed_interval_timestamp_year = {{var("parsed_interval_timestamp_year")}} 
    and parsed_interval_timestamp_month = {{var("parsed_interval_timestamp_month")}} 
    and parsed_interval_timestamp_day = {{var("parsed_interval_timestamp_day")}}
{% endmacro %}

{% macro incremental_filter_clause_for_srdm_hidden_partition() %}
    parsed_interval_timestamp_ts = '{{var("parsed_interval_timestamp_ts")}}'
{% endmacro %}