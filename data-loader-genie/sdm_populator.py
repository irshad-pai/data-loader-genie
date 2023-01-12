import string

class SdmPopulator:
    def __init__(self, data):
        self.sdm_template_file = "templates/sdm_template.sql"
        self.srdm_template_file = "templates/srdm_template.yml"
        self.output_file = "../dbt/sdm_genie/models/sdm/" + data.get("sdm").get('name')+'.sql'
        self.output_yml_file = "../dbt/sdm_genie/models/srdm/" + data.get("srdm").get('name')+'.yml'
        input_config = data.get("sdm")
        input_config['srdm_table_name'] = data.get("srdm").get('name')
        input_config['selectColumns'] = SqlGenerator.get_select_sql(input_config.get('selectColumns'))
        input_config['transformations'] = SqlGenerator.get_transform_sql(input_config.get('transformations').keys(),input_config.get('transformations'))
        input_config['outputColumns'] = SqlGenerator.get_select_sql(input_config.get('outputColumns'))
        self.data = input_config
        SqlGenerator.generate_yml(self.data, self.srdm_template_file, self.output_yml_file)

    def populate(self):
        with open(self.sdm_template_file, 'r') as template_file:
            template = string.Template(template_file.read())
            sql = template.substitute(self.data)
            with open(self.output_file, 'w') as output_file:
                output_file.write(sql)

class SqlGenerator:
    def get_select_sql(columns):
        sql = ""
        if columns:
            sql += ', '.join(columns)
        else:
            sql += "*"
        return sql
    def get_transform_sql(columns, transform_to):
        sql = ""
        for key in columns:
            sql += "{} AS {}, ".format(transform_to[key], key)
        sql = sql[:-1]
        return sql
    def generate_yml(data: dict, template_path: str, output_path: str):
        with open(template_path) as file:
            template = file.read()

        yml_str = template.format(**data)

        with open(output_path, "w") as file:
            file.write(yml_str)




