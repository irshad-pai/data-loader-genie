{% macro get_sdm_audit_fields() %}
    {{ return ("uuid,
                original_string,
                event_timestamp_date as event_timestamp_ts,
                event_timestamp_epoch,
                parsed_interval_timestamp_ts,
                parsed_interval_timestamp,
                ingested_timestamp,
                event_timestamp_offset,
                event_timestamp_iso_client_timezone") }}
{% endmacro %}