# Main class for deploying the sds genie
import sys
import yaml
from sds_nifi_populator import  NifiPopulator


class SDSGenie():
    def run(self, config_path):
        with open(config_path, "r") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        nifi_populator = NifiPopulator()
        nifi_populator.populate(config)
        SrdmPopulator.populate(config)
        SdmPopulator.populate(config)
        OrchestratorPopulate.populate(config)


if __name__ == '__main__':
    config_path = str(sys.argv[1])
    genie = SDSGenie()
    genie.run(config_path)
