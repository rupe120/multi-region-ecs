#!/usr/bin/env python3
import os

import aws_cdk as cdk

from multi_region_ecs.multi_region_ecs_stack import MultiRegionEcsStack

from app_config import app_configuration


app = cdk.App()
for env in app_configuration.envs:    
    for failover_region in env.failover_regions:
        MultiRegionEcsStack(
            app,
            f"{app_configuration.app_name}-{env.name}-{failover_region.region}",
            env_config=env,
            env=cdk.Environment(account=env.account, region=failover_region.region)
        )

app.synth()
