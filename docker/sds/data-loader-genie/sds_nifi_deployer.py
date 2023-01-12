import nipyapi
from nipyapi import canvas,config
from random import randrange

class NifiDeployer():

    def deploy(self):
        nipyapi.config.nifi_config.host = 'http://nifi:8080/nifi-api'
        root_process_group = canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')
        genie_process_group = nipyapi.canvas.get_process_group("General SDS Auto Loader", identifier_type='name',
                                                               greedy=True)
        if genie_process_group is None:

            nipyapi.templates.upload_template(nipyapi.canvas.get_root_pg_id(),
                                              '/sds/nifi/sds_auto_loader.xml')
            egs_template_id = nipyapi.templates.get_template("sds_auto_loader", identifier_type='name', greedy=False).id
            nipyapi.templates.deploy_template(root_process_group.id, egs_template_id, loc_x=randrange(0, 2000),
                                              loc_y=randrange(0, 2000))
            genie_process_group = nipyapi.canvas.get_process_group("General SDS Auto Loader", identifier_type='name',
                                                                   greedy=True)
            all_controllers = nipyapi.canvas.list_all_controllers(pg_id=genie_process_group.id, descendants=True)
            [nipyapi.canvas.schedule_controller(controller, True, refresh=False) for controller in all_controllers]
            nipyapi.canvas.schedule_process_group(genie_process_group.id, True)
