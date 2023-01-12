{% macro get_date(date_column) -%}
    {# date_parse({{ date_column }}, '%Y-%m-%dT%H:%i:%s.%fZ') #}
    from_iso8601_timestamp( {{date_column }})
{%- endmacro %}

{% macro get_epoch_from_date_with_format(date_column,date_format) -%}
    CAST(UNIX_TIMESTAMP({{date_column}},'{{date_format}}') * 1000 AS BIGINT)
{%- endmacro %}

{% macro get_epoch(date_column) -%}
    CAST(UNIX_TIMESTAMP(TO_DATE({{date_column}})) * 1000 AS BIGINT)
{%- endmacro %}

{% macro get_iso8601(date_column) -%}
    TO_DATE({{ get_date(date_column) }}) 
{%- endmacro %}

{% macro get_epoch_from_date_with_custom_format(date_column,date_format) -%}
    CAST(UNIX_TIMESTAMP(TO_DATE({{date_column}},'{{date_format}}')) * 1000 AS BIGINT)
{%- endmacro %}