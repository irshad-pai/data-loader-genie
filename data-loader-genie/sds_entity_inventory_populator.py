import yaml


class EntityInventory():

    def create_sub_array(self, config):
        array_entity = []
        sub_config = {}
        for combination in config:
            for key in combination:
                sub_config['colName'] = key
                sub_config['colExpr'] = combination[key]
                array_entity.append(sub_config)
        return array_entity

    def config_creator(self, config):
        entity_config = {}
        entity_config['primaryKey'] = config.get("sourceInventory").get("person").get("primaryKey")
        entity_config['filterBy'] = config.get("sourceInventory").get("person").get("filterBy")
        entity_config['sourcePrefix'] = config.get("sourceInventory").get("person").get("sourcePrefix")
        entity_config['entityPrefix'] = config.get("sourceInventory").get("person").get("entityPrefix")
        entity_config['origin'] = config.get("sourceInventory").get("person").get("origin")
        entity_inv = EntityInventory()
        entity_config['commonProperties'] = entity_inv.create_sub_array(config.get("sourceInventory").get("person").get("commonProperties"))
        entity_config['entitySpecificProperties'] = entity_inv.create_sub_array(config.get("sourceInventory").get("person").get("entitySpecificProperties"))
        entity_config['sourceSpecificProperties'] = entity_inv.create_sub_array(config.get("sourceInventory").get("person").get("sourceSpecificProperties"))

        print(entity_config)

# if __name__ == '__main__':
#     with open("/home/ajay/Downloads/giga_account.yml", "r") as stream:
#         try:
#             config = yaml.safe_load(stream)
#             genie = EntityInventory()
#             genie.config_creator(config)
#         except yaml.YAMLError as exc:
#             print(exc)
