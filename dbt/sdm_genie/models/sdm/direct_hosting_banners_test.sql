{{ config(
        materialized='incremental',
        unique_key='uuid',
        file_format= "iceberg",
        partition_by = [get_ps_sdm_hidden_partition_clause()],
        post_hook = "ALTER TABLE sdm.direct_hosting_banners_test SET TBLPROPERTIES ('write.spark.accept-any-schema'='true')"
        )
}}
WITH srdm_source_table AS(
    SELECT
            *,
            {{ get_sdm_audit_fields() }}
    FROM {{ source('srdm', 'direct_hosting_banners') }}
    WHERE isValid=true and {{incremental_filter_clause_for_srdm_hidden_partition()}}
),
source_table_transformations AS(
    SELECT *,
        upper(client) AS col2, lower(client) AS col4,
    FROM srdm_source_table
)
SELECT 
    col2, col4 
    from source_table_transformations 
    order by {{get_ps_sdm_hidden_partition_columns()}};