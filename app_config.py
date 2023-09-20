
class RegionConfig(object):
    def __init__(self, region: str):
        self.region = region
class EnvConfig(object):
    def __init__(self, name: str, account: str, failover_regions: list[RegionConfig]):
        self.name = name
        self.account = account
        self.failover_regions = failover_regions
        
class AppConfiguration(object):
    app_name = "cross-region-failover"
    envs = [
        EnvConfig(
            name="dev",
            account="285463978628", 
            failover_regions=
            [
                RegionConfig(region="us-east-1"),
                RegionConfig(region="us-west-2"),
            ]
        )
    ]    

app_configuration = AppConfiguration()
