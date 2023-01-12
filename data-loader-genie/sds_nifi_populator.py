# NIFI execution
import nipyapi
import yaml
from nipyapi import canvas, config
from random import randrange


class NifiPopulator():

    def populate(self, execution_config):
        if "s3" in execution_config.get("source").keys():
            bucket_config = execution_config.get("source").get("s3")
            bucket_name = bucket_config.get("bucket")
            region = "us-west-2"
            object_key = bucket_config.get("objectKey")
            minio_end_point = "http://minio:9000"

            nipyapi.config.nifi_config.host = 'http://localhost:8080/nifi-api'
            genie_process_group = nipyapi.canvas.get_process_group("General SDS Auto Loader", identifier_type='name',
                                                                   greedy=True)
            genie_child_process_groups = nipyapi.nifi.apis.ProcessGroupsApi().get_process_groups(
                genie_process_group.id).process_groups
            receiver_process_group = \
                [child for child in genie_child_process_groups if child.component.name == "Reciever"][0]
            receiver_child_process_groups = nipyapi.nifi.apis.ProcessGroupsApi().get_process_groups(
                receiver_process_group.id).process_groups
            batch_process_group = [child for child in receiver_child_process_groups if child.component.name == "Batch"][
                0]
            batch_child_process_groups = nipyapi.nifi.apis.ProcessGroupsApi().get_process_groups(
                batch_process_group.id).process_groups
            batch_process_group = [child for child in receiver_child_process_groups if child.component.name == "Batch"][
                0]
            batch_child_process_groups = nipyapi.nifi.apis.ProcessGroupsApi().get_process_groups(
                batch_process_group.id).process_groups
            s3_process_group = [child for child in batch_child_process_groups if child.component.name == "S3"][0]
            ad_receiver_pg = nipyapi.canvas.create_process_group(s3_process_group, "AD",
                                                                 (randrange(0, 2000), randrange(0, 2000)),
                                                                 comment='AD S3 process group')
            ad_out_port = nipyapi.canvas.create_port(ad_receiver_pg.id, "OUTPUT_PORT", "ad-out", "STOPPED",
                                                     position=(randrange(0, 2000), randrange(0, 2000)))
            s3_pg_out_ports = nipyapi.canvas.list_all_output_ports(pg_id=s3_process_group.id, descendants=False)
            s3_out_port = [port for port in s3_pg_out_ports if port.component.name == "s3-out"][0]
            nipyapi.canvas.create_connection(ad_out_port, s3_out_port, relationships=None, name=None)
            list_s3_processor = nipyapi.canvas.create_processor(
                parent_pg=ad_receiver_pg,
                processor=nipyapi.canvas.get_processor_type('ListS3'),
                location=(randrange(0, 1000), (randrange(0, 1000))),
                name="ListS3",
                config=nipyapi.nifi.ProcessorConfigDTO(
                    scheduling_period='60 min',
                    execution_node="PRIMARY",
                    comments="List S3 processor",
                    properties={"Bucket": f"{bucket_name}", "Region": f"{region}",
                                "Endpoint Override URL": f"{minio_end_point}",
                                "Credentials File": "/sds/nifi/s3.properties"}
                )
            )
            fetch_s3_processor = nipyapi.canvas.create_processor(
                parent_pg=ad_receiver_pg,
                processor=nipyapi.canvas.get_processor_type('FetchS3Object'),
                location=(randrange(0, 1000), (randrange(0, 1000))),
                name="FetchS3Object",
                config=nipyapi.nifi.ProcessorConfigDTO(
                    scheduling_period='60 min',
                    execution_node="ALL",
                    comments="Fetch S3 processor",
                    auto_terminated_relationships=['failure'],
                    properties={"Object Key": f"{object_key}", "Bucket": f"{bucket_name}", "Region": f"{region}",
                                "Endpoint Override URL": f"{minio_end_point}",
                                "Credentials File": "/sds/nifi/s3.properties"}
                )
            )
            ad_update_attr_processor = nipyapi.canvas.create_processor(
                parent_pg=ad_receiver_pg,
                processor=nipyapi.canvas.get_processor_type('UpdateAttribute'),
                location=(randrange(0, 1000), (randrange(0, 1000))),
                name="UpdateAttribute",
                config=nipyapi.nifi.ProcessorConfigDTO(
                    scheduling_period='0 sec',
                    execution_node="ALL",
                    comments="Updating Attributes to flow file, like source name etc",
                    properties={"data_output_format": "${avro}", "data_type": "${singleline}",
                                "output_storage": "${s3}", "source_name": "ad_json", "split_record": "100"}
                )
            )
            nipyapi.canvas.create_connection(list_s3_processor, fetch_s3_processor, relationships=['success'],
                                             name=None)
            nipyapi.canvas.create_connection(fetch_s3_processor, ad_update_attr_processor, relationships=['success'],
                                             name=None)
            nipyapi.canvas.create_connection(ad_update_attr_processor, ad_out_port, relationships=['success'],
                                             name=None)
            nipyapi.canvas.schedule_process_group(s3_process_group.id, True)
