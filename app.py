#!/usr/bin/env python3

import aws_cdk as cdk
import os

from stack.application_stack import ApplicationStack

stack_name = "acme-app-demo"
app = cdk.App()

ApplicationStack(app, stack_name)

app.synth()
