import logging
import json
import os
import io
import minio
class SrdmPopulator:
    def populate(self,dictionary):
        base_path=os.getenv(key='SDS_WAREHOUSE_PATH')
        srdm_schema_name="srdm"
        sdm_schema_name="sdm"
        if dictionary["srdm"]:
            if dictionary["srdm"]["name"]:
                source_name=dictionary["srdm"]["name"]
            else:
                logging.warning('source name is not specified')
        else:
            logging.warning('srdm configuration is not specified')
        if dictionary.get("srdm", {}).get("transformationConfig"):
            spark_config = {
                "rdmPath": f"{base_path}/rdm/{source_name}/",
                "srdmTableName": f"{srdm_schema_name}.{source_name}",
                "sdmTableName": f"{sdm_schema_name}.{source_name}",
                "transformationConfig": {
                    "event_timestamp_epoch": dictionary["srdm"]["transformationConfig"]
                }
            }
        else:
            spark_config = {
                "rdmPath": f"{base_path}/rdm/{source_name}/",
                "srdmTableName": f"{srdm_schema_name}.{source_name}",
                "sdmTableName": f"{sdm_schema_name}.{source_name}",
                "transformationConfig": {
                    "event_timestamp_epoch": "ingested_timestamp"
                }
            }

        data_source_config=json.dumps(spark_config,indent=2)

        client = minio.Minio(
            endpoint=os.getenv(key='MINIO_ENDPOINT_URL',default='minio:9000'),
            access_key=os.getenv(key='MINIO_ACCESS_KEY',default='minioadmin'),
            secret_key=os.getenv(key='MINIO_SECRET_KEY',default='minioadmin'),
            secure=False
        )
        data_as_bytes = data_source_config.encode('utf-8')
        data_as_a_stream = io.BytesIO(data_as_bytes)

        result = client.put_object(
            "sds", f"spark_config/{source_name}",data_as_a_stream , length=len(data_as_bytes),
            content_type="application/json"
        )












