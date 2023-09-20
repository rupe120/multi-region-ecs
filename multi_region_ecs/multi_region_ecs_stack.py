from aws_cdk import (
    Duration,
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_iam as iam,
)
from constructs import Construct

from app_config import app_configuration, EnvConfig

class MultiRegionEcsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_config: EnvConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ECS Cluster for AWS API proxy
        cluster = ecs.Cluster(
            self, 
            "ProxyCluster",
            container_insights=True,
            enable_fargate_capacity_providers=True,
        )
        
        api_poxy_image = ecs.ContainerImage.from_asset('src/proxy_container_image')
        
        
        # Dictionary comprehension to create a dictionary of User Pool ID environment variables for the ECS task
        env_vars = {}
        env_vars["ACCOUNT_ID"] = env_config.account
        env_vars["FAILOVER_REGIONS"] = ",".join([region.region for region in env_config.failover_regions])
        
        # ECS Fargate Service for AWS Cognito API proxy
        cognito_proxy_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "AwsApiProxySecureService",
            cluster=cluster,
            cpu=256,
            desired_count=1,    
            max_healthy_percent=300,        
            memory_limit_mib=512,
            task_image_options={
                "image": api_poxy_image,
                "container_port": 8000,
                "enable_logging": True,
                "environment": env_vars
            },          
        )
        
        cognito_proxy_service.target_group.configure_health_check(
            interval=Duration.seconds(300)
        )
