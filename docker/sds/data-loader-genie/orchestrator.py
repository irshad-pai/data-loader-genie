
import os
from string import Template

class Orchestrator():

    def populate(config):
        input_dict = config.get('srdm')
        input_dict['source'] =config.get("source").get("name")
        input_dict['className'] = config.get('srdm').get('parserClassName')
        input_dict['sdmName'] = config.get('sdm').get('name')
        input_dict['cron'] = config.get('orchestration').get('cron')
        input_dict['srdm_source'] = config.get('srdm').get('name')


        template_file = "templates/dag_template.py"
        output_file = "/sds/airflow/dags/sds_dataloader/"+config.get("source").get("name")+".py"
        with open(template_file, 'r') as f:
            template_str = f.read()
        t = Template(template_str)
        populated_str = t.substitute(input_dict)
        with open(output_file, 'w') as f:
            f.write(populated_str)

#args = {"source":{"name":"source_name"},"orchestration":{"cron":"1"},"srdm":{"name":"direct_hosting_banners","parserClassName":"p"},"sdm":{"name":"direct_hosting_banners_test","transformations":{"col2":"upper(client)","col4":"lower(client)"},"outputColumns":{"col2","col4"}}}

#Orchestrator.populate(args)