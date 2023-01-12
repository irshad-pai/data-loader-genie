Data Loader Genie

-----------------
SdmPopulator

Example:
args = {"srdm":{"name":"direct_hosting_banners"},"sdm":{"name":"direct_hosting_banners_test","transformations":{"col2":"upper(client)","col4":"lower(client)"},"outputColumns":{"col2","col4"}}}

sdm_populator = SdmPopulator(args)
sdm_populator.populate()

This will populate sdm model and srdm source yml file inside data-loader-genie/dbt/srdm_genie project

#env variable
SPARK_THRIFT_HOST <- from env variables
-----------------