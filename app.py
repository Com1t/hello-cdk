#!/usr/bin/env python3
import aws_cdk as cdk

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    Duration
)
from constructs import Construct


class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.create_lambda(construct_id)

    def create_lambda(self, construct_id: str):
        base_lambda = _lambda.DockerImageFunction(self, f'{construct_id}-lambda',
                                                  code=_lambda.DockerImageCode.from_image_asset(r'./'),
                                                  timeout=Duration.seconds(30),
                                                  function_name=f'{construct_id}-lambda'
                                                  )
        return base_lambda


app = cdk.App()
stack_name = "repo-name-branch-name"
LambdaStack(app, stack_name, env=cdk.Environment(account='****', region='us-east-1'))

app.synth()
