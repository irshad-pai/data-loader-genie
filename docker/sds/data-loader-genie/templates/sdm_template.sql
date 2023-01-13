{{ config(
        materialized='incremental',
        unique_key='uuid',
        file_format= "iceberg",
        partition_by = [get_ps_sdm_hidden_partition_clause()],
        post_hook = "ALTER TABLE sdm.$name SET TBLPROPERTIES ('write.spark.accept-any-schema'='true')"
        )
}}
WITH srdm_source_table AS(
    SELECT
            $selectColumns,
            {{ get_sdm_audit_fields() }}
    FROM {{ source('srdm', '$srdm_table_name') }}
),
source_table_transformations AS(
    SELECT * $transformations
    FROM srdm_source_table
)
SELECT 
    $outputColumns , {{ get_sdm_audit_fields() }}
    from source_table_transformations 
    order by {{get_ps_sdm_hidden_partition_columns()}};