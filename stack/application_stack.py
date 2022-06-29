import os
from inspect import cleandoc
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as _iam,
    aws_cognito as cognito,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    CfnOutput
)

extra_config = {
    'cors_white_list': [
        'http://localhost:9000',
        'http://localhost:8765',
        'https://example.com',
        'https://www.example.com',
    ]
}

class ApplicationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        '''
        Defines the AWS cloud stack.

            Parameters:
                scope: normally this will be a cdk.App instance which will be used to synthesize the stack
                construct_id: the name of the stack.  This is used as the prefix for the name of most artifacts in the stack.
                    (If the value is a hyphenated string it will be converted to a camelized string before being used as the name prefix.)
        '''
        super().__init__(scope, construct_id, **kwargs)
        if ('-' in construct_id):
            self.stack_name_prefix = ''.join([ s.capitalize() for s in construct_id.split('-')])
        else:
            self.stack_name_prefix = construct_id
        self.create_lambda_parameter_templates()
        user_pool = self.create_user_pool()
        user_pool_client = self.create_user_pool_client(user_pool)
        # self.create_user_pool_domain(user_pool)
        user_table = self.create_user_data_table()
        user_data_lambda_role = self.create_user_data_lambda_role(user_table)
        user_data_post_lambda = self.create_write_user_data_lambda(user_table, user_data_lambda_role)
        user_data_get_lambda = self.create_get_user_data_lambda(user_table, user_data_lambda_role)
        user_api = self.create_user_api(
            data_post_lambda = user_data_post_lambda,
            data_get_lambda = user_data_get_lambda,
            user_pool=user_pool
        )
        CfnOutput(self, 'IDOfTheAPI', export_name=f'{self.stack_name_prefix}-IDOfTheAPI', value=user_api.rest_api_id)
        CfnOutput(self, 'URLOfTheAPI', export_name=f'{self.stack_name_prefix}-URLOfTheAPI', value=user_api.url)
        CfnOutput(self, 'TheUserPoolId', export_name=f'{self.stack_name_prefix}-TheUserPoolId', value=user_pool.user_pool_id)
        CfnOutput(self, 'TheUserPoolClientId', export_name=f'{self.stack_name_prefix}-TheUserPoolClientId', value=user_pool_client.user_pool_client_id)
        CfnOutput(self, 'UserDataTableName', export_name=f'{self.stack_name_prefix}-UserDataTableName', value=user_table.table_name)

    def create_lambda_parameter_templates(self):
        '''
            Creates the velocity templates used to marshal the parameters for the lambdas.

            As well as rearranging the input parameters these also inject the user sub (effectively the
            user pool id) from the authorizer. This has the effect of making it impossible to create records
            in somebody else's account unless the OAuth tokens are hijacked.
        '''
        self.post_template_with_user_sub = cleandoc("""
            #set($inputRoot = $input.path('$'))
            {
                "userSub": "$context.authorizer.claims.sub",
                "recordType": "$inputRoot.type",
                "epochTime": "$inputRoot.time",
                "document": $input.json('$.doc')
            }
        """)

        self.get_template_with_user_sub_time_params = cleandoc("""
            #set($inputRoot = $input.path('$'))
            {
                "userSub": "$context.authorizer.claims.sub",
                "recordType": "$util.escapeJavaScript($input.params('type'))",
                "fromTime": "$util.escapeJavaScript($input.params('from'))",
                "toTime": "$util.escapeJavaScript($input.params('to'))"
            }
        """)


    def create_user_pool(self):
        ''' Cognito UserPool for the stack. This will be named using the stack name prefix + 'UserPool' + a random id string.'''
        pool_name = self.stack_name_prefix + 'UserPool'
        user_pool = cognito.UserPool(self,
            pool_name,
            self_sign_up_enabled = True,

            standard_attributes = cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=False
                )
            )
        )
        return user_pool

    def create_user_pool_domain(self, user_pool):
        '''
        Create a domain for the user pool.  This is useful if using the hosted html and can be omitted if not.
        '''
        return user_pool.add_domain('Domain',
            cognito_domain=cognito.CognitoDomainOptions(domain_prefix=self.stack_name_prefix.lower())
        )

    def create_user_pool_client(self, user_pool):
        '''
        Create the client for the user pool.  This is used to manage OAuth flows and settings and is used by
        the gateway authorizer.  The callback urls that will be allowed by the hosted html are currently
        hard-coded inside this method. If you are using the hosted HTML for real you will probably want to
        change this.
        '''
        client = user_pool.add_client('Client',
            o_auth = cognito.OAuthSettings(
                flows = cognito.OAuthFlows(
                    authorization_code_grant = True,
                    implicit_code_grant = True
                ),
                scopes = [
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.COGNITO_ADMIN,
                ],
                callback_urls = [ 'https://example.com/callback', 'http://localhost:9000' ],
                logout_urls = [ 'https://example.com/signout' ]
            ),
            supported_identity_providers = [ cognito.UserPoolClientIdentityProvider.COGNITO ]
        )
        cfn_client = client.node.default_child
        cfn_client.add_property_override("ExplicitAuthFlows", [
                "ALLOW_ADMIN_USER_PASSWORD_AUTH",
                "ALLOW_REFRESH_TOKEN_AUTH",
                "ALLOW_USER_SRP_AUTH",
                "ALLOW_USER_PASSWORD_AUTH"
            ]
        )
        return client

    def create_user_data_lambda_role(self, user_data_table):
        '''
        A role for the two user data lambdas.  In addition to two standard managed policies this
        role is allowed to PutItem() and (Query) on the DynamoDB table.
        '''
        write_to_user_data_policy = _iam.PolicyDocument(
            statements = [
                _iam.PolicyStatement(
                    effect = _iam.Effect.ALLOW,
                    actions = [ "dynamodb:PutItem", "dynamodb:Query"  ],
                    resources = [ user_data_table.table_arn ]
                )
            ]
        )
        role_name = self.stack_name_prefix + 'UserDataLambdaRole'
        lambda_role = _iam.Role(scope=self,
            id=role_name,
            assumed_by =_iam.ServicePrincipal('lambda.amazonaws.com'),
            role_name=role_name,
            inline_policies = [ write_to_user_data_policy ],
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaVPCAccessExecutionRole'),
                _iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
            ])
        return lambda_role

    def create_write_user_data_lambda(self, user_data_table, lambda_role):
        ''' The lambda which implements POST action on the user data resource.'''
        return self.create_lambda(lambda_name = f'{self.stack_name_prefix}-WriteUserDataLambda',
            code_location = 'write_user_data',
            description = 'Lambda function handling user data POSTs for web client.',
            handler_string = 'write_user_data.handler',
            lambda_role = lambda_role,
            environment_map = {
                'DATA_TABLE_NAME': user_data_table.table_name,
                'USER_DATA_WRITE_TYPES': '[ "LOG", "ERROR", "LEVEL", "FEEDBACK" ]'
            })

    def create_get_user_data_lambda(self, user_data_table, lambda_role):
        ''' The lambda which implements GET action on the user data resource.'''
        return self.create_lambda(lambda_name = f'{self.stack_name_prefix}-GetUserDataLambda',
            code_location = 'get_user_data',
            description = 'Lambda function handling user data GETs for web client.',
            handler_string = 'get_user_data.handler',
            lambda_role = lambda_role,
            environment_map = {
                'DATA_TABLE_NAME': user_data_table.table_name,
                'USER_DATA_READ_TYPES': '[ "LOG", "ERROR", "LEVEL", "FEEDBACK", "SUBSCRIPTION" ]'
            })

    def create_lambda(self, lambda_name, code_location, description, handler_string, lambda_role, environment_map):
        ''' Utility method to do the CDK level lambda creation.'''
        return _lambda.Function(self,
            lambda_name,
            runtime = _lambda.Runtime.PYTHON_3_9,
            function_name = lambda_name,
            description = description,
            code =_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'lambda', code_location)),
            handler = handler_string,
            role=lambda_role,
            environment = environment_map
        )

    def standard_200_400_method_responses(self):
        '''
        Utility method returns standard method response definitions for 200 OK and 400 SNAFU.

        These are public facing gateway method responses (as opposed to the internal integration method responses.)
        '''
        return [
            apigateway.MethodResponse( status_code = "200",
                response_parameters =  {
                    "method.response.header.Access-Control-Allow-Headers": True,
                    "method.response.header.Access-Control-Allow-Origin": True
                }
            ) ,
            apigateway.MethodResponse( status_code = "400",
                response_parameters =  {
                    "method.response.header.Access-Control-Allow-Headers": True,
                    "method.response.header.Access-Control-Allow-Origin": True
                }
            )
        ]

    def standard_200_400_integration_responses(self):
        '''
        Utility method returns standard method response definitions for 200 OK and 400 SNAFU in the integration layer.

        These are internal integration method responses (as opposed to the public facing gateway method responses.)
        '''

        return [
            apigateway.IntegrationResponse( status_code = "200",
                response_parameters =  {
                    "method.response.header.Access-Control-Allow-Headers":
                        "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'",
                    "method.response.header.Access-Control-Allow-Origin": "'*'"
                }
            ),
            apigateway.IntegrationResponse( status_code = "400",
                selection_pattern = ".*400_BAD_REQUEST.*",
                response_parameters =  {
                    "method.response.header.Access-Control-Allow-Headers":
                        "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'",
                    "method.response.header.Access-Control-Allow-Origin": "'*'"
                }
            )
        ]

    def create_user_api(self, data_post_lambda, data_get_lambda, user_pool):
        '''
        The API for users - ie. customers.
        '''
        authorizer_name = self.stack_name_prefix + 'UserDataAuthorizer'
        api_name = 'UserApi'

        user_authorizer = apigateway.CognitoUserPoolsAuthorizer(self,
            authorizer_name,
            cognito_user_pools = [ user_pool ]
        )
        api = apigateway.RestApi(self,
            api_name,
            rest_api_name = self.stack_name_prefix + 'UserApi',
            endpoint_configuration = apigateway.EndpointConfiguration(types = [
                apigateway.EndpointType.REGIONAL
                ]
            )
        )
        api.add_gateway_response('response_for_4xx',
            type=apigateway.ResponseType.DEFAULT_4_XX,
            status_code="400",
            response_headers={
                "Access-Control-Allow-Headers":
                    "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'",
                "Access-Control-Allow-Origin": "'*'"
            }
        )

        user_data_resource = api.root.add_resource('user-data')
        user_data_resource.add_cors_preflight(
            allow_origins = extra_config['cors_white_list'],
            allow_headers=[ 'Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key' ],
            allow_methods=[ 'GET', 'POST' ]
        )

        self.add_lambda_resource_method(gateway_resource = user_data_resource,
            http_verb = 'POST',
            lambda_instance = data_post_lambda,
            request_template = self.post_template_with_user_sub ,
            gateway_authorizer = user_authorizer)

        self.add_lambda_resource_method(gateway_resource = user_data_resource,
            http_verb = 'GET',
            lambda_instance = data_get_lambda,
            request_template = self.get_template_with_user_sub_time_params,
            gateway_authorizer = user_authorizer)

        return api

    def add_lambda_resource_method(self, gateway_resource, http_verb, lambda_instance, request_template, gateway_authorizer):
        ''' Utility method which adds a lambda implemented method to an API Gateway resource object.'''
        return gateway_resource.add_method(http_verb,
            apigateway.LambdaIntegration(
                lambda_instance,
                proxy=False,
                request_templates = {
                    "application/json": request_template
                },
                integration_responses = self.standard_200_400_integration_responses()
            ),
            method_responses = self.standard_200_400_method_responses(),
            authorizer = gateway_authorizer,
            authorization_scopes = [ 'email', 'aws.cognito.signin.user.admin' ]
        )

    def create_user_data_table(self):
        table_name = self.stack_name_prefix + 'UserData'
        table = dynamodb.Table(self, table_name,
            partition_key = dynamodb.Attribute(name = 'TypeUserSub',
                type = dynamodb.AttributeType.STRING
            ),
            sort_key = dynamodb.Attribute(name='EpochTime',
                type = dynamodb.AttributeType.NUMBER
            ),
            billing_mode = dynamodb.BillingMode.PAY_PER_REQUEST
        )
        return table
