import aws_cdk as core
import re
import pytest
from aws_cdk.assertions import Template, Capture
from stack.application_stack import ApplicationStack

@pytest.fixture()
def application_template():
    app = core.App()
    stack = ApplicationStack(app, "acme-app-demo")
    yield Template.from_stack(stack)

def test_stack_has_an_api_gateway_with_correct_name(application_template):
    application_template.has_resource_properties("AWS::ApiGateway::RestApi" , {
        "Name": "AcmeAppDemoUserApi"
    })

def test_api_gateway_has_one_resource_with_correct_path(application_template):
    application_template.resource_count_is("AWS::ApiGateway::Resource", 1)
    captured_rest_api_id = Capture()
    application_template.has_resource_properties("AWS::ApiGateway::Resource" , {
        "PathPart": "user-data",
        "RestApiId": {
            "Ref": captured_rest_api_id
        }
    })
    assert re.match("^UserApi", captured_rest_api_id.as_string())

def test_user_data_resource_at_root_of_api(application_template):
    captured_parent_root_resource = Capture()

    application_template.has_resource_properties("AWS::ApiGateway::Resource" , {
        "PathPart": "user-data",
        "ParentId": {
            "Fn::GetAtt": [
                captured_parent_root_resource,
                "RootResourceId"
            ]
        },
    })
    assert re.match("^UserApi", captured_parent_root_resource.as_string())

def test_user_data_resource_has_get_post_options_methods(application_template):
    application_template.resource_count_is("AWS::ApiGateway::Method", 3)
    application_template.has_resource_properties("AWS::ApiGateway::Method" , { "HttpMethod": "OPTIONS" })
    application_template.has_resource_properties("AWS::ApiGateway::Method" , { "HttpMethod": "GET" })
    application_template.has_resource_properties("AWS::ApiGateway::Method" , { "HttpMethod": "POST" })

def test_api_options_method_permits_first_listed_allowed_origin(application_template):
    application_template.has_resource_properties("AWS::ApiGateway::Method" , {
        "HttpMethod": "OPTIONS",
        "Integration": {
           "IntegrationResponses": [ {
               "ResponseParameters": {
                   "method.response.header.Access-Control-Allow-Origin": "'http://localhost:9000'",
                   "method.response.header.Vary": "'Origin'"
               }
           } ]
        }
    })

def test_api_options_method_permits_get_post(application_template):
    application_template.has_resource_properties("AWS::ApiGateway::Method" , {
        "HttpMethod": "OPTIONS",
        "Integration": {
           "IntegrationResponses": [ {
               "ResponseParameters": {
                   "method.response.header.Access-Control-Allow-Methods": "'GET,POST'"
               }
           } ]
        }
    })

def test_api_post_method_is_authorized_by_cognito(application_template):
    captured_authorizer_id = Capture()
    application_template.has_resource_properties("AWS::ApiGateway::Method" , {
        "HttpMethod": "POST",
        "AuthorizationScopes": [
            "email",
            "aws.cognito.signin.user.admin"
        ],
        "AuthorizationType": "COGNITO_USER_POOLS",
        "AuthorizerId": {
            "Ref": captured_authorizer_id
        }
    })
    assert re.match("^AcmeAppDemoUserDataAuthorizer", captured_authorizer_id.as_string())

def test_api_post_method_integrates_lambda(application_template):
    captured_lambda_name = Capture()
    application_template.has_resource_properties("AWS::ApiGateway::Method" , {
        "Integration": {
            "IntegrationHttpMethod": "POST",
            "Type": "AWS",
            "Uri": {
              "Fn::Join": [
                "",
                [
                  "arn:",
                  {
                    "Ref": "AWS::Partition"
                  },
                  ":apigateway:",
                  {
                    "Ref": "AWS::Region"
                  },
                  ":lambda:path/2015-03-31/functions/",
                  {
                    "Fn::GetAtt": [
                      captured_lambda_name,
                      "Arn"
                    ]
                  },
                  "/invocations"
                ]
              ]
            }
        }
    })
    assert re.match("^AcmeAppDemoWriteUserDataLambda", captured_lambda_name.as_string())




