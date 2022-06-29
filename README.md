# acme-app-demo

This repo provides a demonstration app that may be useful as a bootstrap backend for many kinds of online enterprises.  It is an AWS based stack consisting of API Gateway, some Lambdas, a Cognito User Pool and DynamoDB Table. The code here is largely modelled on a real world app: tunasoniq.io (“the learning music app”).  Tunasoniq’s own code base is proprietary and Acme App Demo is MIT licensed, there is no ongoing dependency between the two. Feel free to use the code in this repo without encumbrance.

Acme App Demo is Python-centric. It uses Cloud Development Kit (CDK) code in Python and the Lambdas are also in Python.  CDK code can also be written in TypeScript, JavaScript, Java, C#/.Net or GoLang if those languages are more suitable for your organisation.  You can also write Lambdas in all of those languages as well as PowerShell.

There are lots ways and lots of platforms to get an enterprise-grade backend off the ground - starting with an AWS cloud stack is just one.

Building a new application on AWS is appealing for a lot of reasons and it is the route many businesses take - but getting to the starting line with AWS can be a big ask for small startups teams especially if their main focus is on delivering front-end experience.

AWS have a solution for this - it’s called Amplify.  Amplify gets a lot of traction and a lot of serious businesses have been built on it but - cards on table - I do not like Amplify.  Amplify is a highly opinionated framework and, as with your Brexit or Trump voting uncle, it is often difficult to understand why it holds those opinions.  I have seen businesses, who probably should have known better, going a long way down the wrong path because of decisions taken for them by Amplify.  Amplify is also held together with secret spider glue (or at least it appears to be): there are parts of an Amplify app that are strangely opaque and painful to refactor when your startup moves up to a bigger league.

It ought to be fairly easy, with a little bit of effort, to build an app like an Amplify app but with a more transparent tool set.  AWS’s main tool for wrangling cloud stacks is CloudFormation (CFN) which uses JSON or YAML configuration files to build your stack. More recently the AWS developer community has embraced CloudDeveloperKit (CDK). CDK allows you to write configuration-as-code in several popular languages. CDK generates and manages CFN files on your behalf.  If you need to move away from CDK you can simply extract the CFN files to create a clean break.

The CDK code is going to be terser than the corresponding CFN and is likely to be more malleable - if you want to make changes, especially far-reaching changes, it will be easier in CDK than raw CFN.

However, it turns out to be far from easy, starting from scratch, to build a CDK app that delivers the same features as a simple Amplify app, mainly because there just are a lot of wrinkles and pitfalls in slotting the AWS components together.  Not all of those wrinkles and pitfalls are clearly documented and, because AWS tries really hard to be an open platform with lots of languages and tools and approaches, even when things are documented it can be a challenge to find just the nugget you need.

So that is why Acme App Demo is here. It creates a stack with four main components:

  - user authentication with a Cognito User Pool
  - an API Gateway for users, with an OAuth authorizer
  - a couple of Lambdas accessed via the API Gateway
  - a user data store in the form of a DynamoDB table.

There is also a smoke test which will create a test user and then launch a demo web page which allows you to exercise most of the deployed code.

Not everything here is 100% ready for production. I’ve tried to point out areas where you may want to further lock down and configure the code before releasing it into the wild. Some tests are included and there are some ideas on how you can develop a production ready testing strategy (see below).

That said, I hope it gets you to within sight of the starting line relatively quickly and painlessly.

## Requirements
#### Clone the Repo
```
cd your-work-directory
git clone https://github.com/tonyxyz/acme-app-demo.git
cd acme-app-demo
```
#### AWS
If you are not yet set up with an AWS account, read their own [getting started](https://aws.amazon.com/getting-started/) guide. You should set up a user within your AWS account who has permissions to create and run CDK apps and make this user your default user locally. The usual way to do this is to edit ` ~/.aws/credentials`.

If you work through the setup tutorials in the AWS link above you will have this.

If you have a new account that qualifies for the free tier you can probably setup and test Acme App Demo for free, if not it will maybe cost you a few pennies.

Of course, when you have millions of users and terabytes of application data it will cost you a lot more but, by that stage, you will have many interesting problems.

#### NodeJS
NodeJS is required by the core CDK cli app. (The smoke test web page does not require NodeJS to build.)

You need a fairly up-to-date NodeJS/NPM installation. There is a .nvmrc file in the root of the project that specifies v18.2.0. If you have nvm installed and Node 18.2.0 you can just type.
```
nvm use
```
And if that means nothing to you - probably go and find a good tutorial on installing NodeJS, npm and nvm.

Once your NodeJS environment is good install the CDK core and run the help to check and familiarise:
```
npm install -g aws-cdk
cdk help
```

#### Cognito Client Library
The one AWS javascript library we use in the test client is amazon-cognito-identity-js.  It can be useful to have the source code for this to hand as it really is the best documentation.

If you are happy to create an npm project in the source directory, do this:
```
npm init
npm install amazon-cognito-identity-js
```
After which you can read the source in `node_modules/amazon-cognito-identity-js/src`.

In the test web client we simply include the minified version, amazon-cognito-identity.min.js copied directly from the node module.  Once you are building a real world client you will probably want to include the library in that - and, of course, you can read the source code from there.

#### Python

The latest version of Python currently supported in AWS Lambda (at the time of writing) is 3.9 so it makes sense to set up a virtual environment using 3.9 to contain the project dependencies. If your local python is based on pyenv do something like this:

```
pyenv install --list
pyenv install 3.9.12
pyenv global 3.9.12
python --version
```
Or, if you are an opinionated python developer, do something equivalent.

When you create a Python CDK project  from scratch using
```
cdk init app --language=python
```
CDK will create a venv virtual environment for you in .venv/ . You can do the same here using
```
python3 -m venv .venv
source .venv/bin/activate
```
Or if you currently use pyenv-virtualenv or conda for managing virtual environments these will probably work equally well.

Then, with your new virtual environment active, run:
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Creating the stack

To create the stack run:

```
cdk deploy
```

## Running the Tests

### 'Unit' Tests

The project includes a small number of tests that you can run using:
```
python -m pytest --no-header -v
```

These tests follow the methodology used by the example CDK tests created by `cdk init`. They test whether the CloudFormation code output by our CDK match expections.

I decided not to write a comprehensive set of tests like this for two reasons:

Firstly it is not feasible for most people to write real up-front unit tests like this unless one has a really expert knowledge of CloudFormation JSON.  ie. It is difficult to see how developers could realistically do Test Driven Development like this.

Full discloure: these tests were written post-hoc.

Secondly all the tests are really doing is that the code renders an output document in line with expectations. A simpler way of doing this would be to do a full snapshot test of the rendered stack.

It would be great if there were a fully featured assertion library to facilitate real TDD against the rendered CFN code but, as far as I am aware, such a library does not yet exist.

### Smoke Test

Also provided is a smoke test that runs through the key features of the stack. Run it after creating the stack.

First it creates a new user with a known temporary password then it renders a web page in a live web server allowing you to changed the password, complete login, write and read data and logout.

```
./tests/smoke/create_user_and_records.py
```

The login and logout behaviour leverages amazon-cognito-identity-js and the api calls are all done through native javascript code using fetch() in this case though in a real client you will probably use your client framework to do this.

This approach to testing could be extended by running the client with Selenium and a Business Driven Development, BDD, framework of your choice.

## About The Stack

You can examine the newly created stack in the AWS Console, navigate to CloudFormation, choose Stacks from the side menu and then open up acme-app-demo. Open the Resources tab to see a list of things created in the stack.

There are around twenty individual resources. The majority of these are things we have created explicitly in the code, there is also some default plumbing created by CDK.

### User Pool

The AcmeAppDemoUserPool is a fairly minimal user pool. It is configured in a such a way that the only user details we capture are the email address and this is also used as the username.

Users will receive a sign up email from the user pool and can also receive forgotten password links and suchlike if you go on to implement these. Notice that although the user pool can send these emails directly you are explicitly warned against doing this in production in the console.

In application_stack.py create_user_pool() is the method that creates this.

[UserPool CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cognito/UserPool.html)

[UserPool CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpool.html)

### User Pool Domain and Hosted HTML

One way of allowing users to sign up and sign in is to used the hosted HTML provided by User Pool.  Basic code to support this is included in the stack - although the line to create the UserPoolDomain is commented out. You will need to give your stack and/or domain a unique name to avoid name collisions with other people running AcmeAppDemo in the same AWS region as you.

The hosted HTML is not very flexible and probably won't be a good fit for a well styled consumer web app.  Additionally it cannot be placed inside an <iframe> element so, unless you are developing a very utilitarian web app, you probably don't want it.

It can be useful during testing and development though.

[UserPoolDomain CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cognito/UserPoolDomain.html)

[UserPoolDomain CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpooldomain.html)

### User Pool Client

On its own a User Pool is fairly uncommunicative.  You will need a UserPoolClient for the web app to talk to.

The UserPoolClient also works with the UserPoolDomain, if you have one, to authorize redirect urls that you pass to the hosted HTML.

You should check that the callback_urls and logout_urls created in create_user_pool_client() match your security requirements.

The client allows the use of two different OAuth scopes. When the user logs in with their password we are ultimately relying on email authentication so the scope in the OAuth access token is EMAIL. If you configure your user pool to allow third party logins or SMS codes and so forth you will need to allow other scopes.

If a user is logged in by a backend client using an IAM identity the OAuth scope will be COGNITO_ADMIN. You may need this scope if and when you build a support app for Customer Service, for instance.

You should review your security requirements.

Notice that CDK does not always allow the fine grained control that CFN does.  In this case we need to access features in the underlying CFN to change the ExplicitAuthFlows.

[UserPoolClient CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cognito/UserPoolClient.html)

[UserPoolClient CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cognito-userpoolclient.html)

### DynamoDB Table

There is a NoSQL concept that the correct design is always one table.  In the Acme App Demo design we have a single user table to store data regarding purchases, user performance, routine activity logs and errors. It is important to think through the use cases required of the table in advance.

In our case we propose the system needs to give an up-to-date view of the user's subscription status, possibly purchases, active engagement with the app, level of acheivement, user feedback provided, system errors encountered.

Additionally any or all of these user data types may need to be viewed by time slice.

The table has a partition key composed of the record type and user's id from the user pool, which is a GUID.  A typical value would be 'LOG::cb53b9fc-953c-488b-a477-0ce5e5551649'.  The name of this field is TypeUserSub.

The sort key on the table is the time expressed as 'epoch seconds' or unix time, ie. seconds since the beginning of 1970. It is occasionally possible for records to share the same partition-key-sort-key pair but this does not present any practical problems. The name of the sort key field is EpochTime.

The functional content of a record is provided in an unindexed field named 'Doc' which is expected to contain JSON data.  Additionally we may sometimes add another field to the record.  For instance when the user makes a subscription payment we might create a user visible document containing the date, subscription period and amount in the Doc field and store the more detailed source payment record from the payment service provider in a seperate 'PaymentDoc' field.

Only the Doc field is returned via the user-facing API methods.

[DynamoDB Table CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html)

[DynamoDB Table CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html)

### RestAPI

API gateway resource consist of several active components. In the demo app it has an authorizer, a single resource object 'user-data' with two methods explicitly attached, GET and POST, the api also supports and OPTIONS method which is implicitly created by the CORS configuration.

The gateway integrates with two lambdas to implement read and write operations.

There is a 4xx response attached to the RestAPI to allow the gateway to return errors, for instance when authorization fails. We also have response types at method level to handles 2xx and 4xx responses from the gateway resource methods and at the integration level to handle responses from implementing lambdas.

API Gateway objects are released using Stage and Deployment objects. If you are tweaking an API Gateway in the console you need to think about these objects but in the normal course of events CDK just takes care of them. You can see them in the stack in the console.

[API Gateway Rest API CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-restapi.html)

[API Gateway Rest API CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/RestApi.html)

#### CognitoUserPoolsAuthorizer

The authorizer accepts or rejects a request to a gateway method by checking the access token against the grant made by the UserPool.  By default this expects to find an access token in an HTTP header named Authorization, which is what we do, so no further configuration is needed here.

This reads slightly differently in CDK and CFN. CDK provides a specific CognitoUserPoolsAuthorizer class but what it generates in CFN is an APIGateway::Authorizer resource with the type set to COGNITO_USER_POOLS.

[APIGateway Authorizer CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-authorizer.html)

[CognitoUserPoolsAuthorizer CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/CognitoUserPoolsAuthorizer.html)

#### Gateway Resource

A resource represents a named path in the REST api which is conceptually linked to a resource type on which Create-Read-Update-Delete (CRUD) operations can be performed.  On its own it does nothing - we attach Methods to it to implement the operations we want.

In CDK we can also create Cross Origin Resource Sharing (CORS) configuration which is a browser security feature designed to help protect against cross-site scripting attacks.

CDK implements an add_cors_preflight() on the Resource type which creates OPTIONS method to handle cors preflight requests. In the corresponding CFN output what it actually does is write out a the headers in a template inside the OPTIONS method object.

There is no corresponding helper method in the explicit Method object.

The approach we have taken here is to use the cors preflight method to lock down the allowed origins and then just return '*' on the Method objects. It should be possible to replicate the add_cors_preflight() implementation on the Method objects if your security model requires that degree of control.

[APIGateway Resource CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Resource.html)

[APIGateway Resource CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-resource.html)

#### Gateway Resource Methods

There are two methods GET and POST.  The implementation is nearly identical: we use Resource.add_method() with a Lambda integration.

When proxy is set to true on the integration the gateways passes the request through to the lambda unchanged.  We set it to false and this allows us to manipulate the input parameters and request body. Crucially we can pass the user sub field from the authorizer into the lambda as part of the request: 'sub' is OAuth terminology for subject or user id, here that is the id field from the User Pool.  The effect of this is that lambda gets the user id with Cognito's assurance that it is the real value.

The rewriting of the request parameters and/or body is done in using Apache Velocity templates attached to the LambdaIntegration for each method.

In the case of the POST method we inject the user sub and shuffle the request document around a bit. In the case of the GET method we create a request document from the URL parameters and the user sub - GET methods are not allowed to have their own body in standard HTTP.

So we can take a GET request like `www.acmeappdemo.com/user-data?type=LOG&from=1656499428&to=1656503028` and create a request body like
```
  {
    "userSub": "ff64d008-4c4a-4ab7-8d29-b16a74100bf0",
    "recordType": "LOG",
    "fromTime": 1656499428,
    "toTime": 1656503028"
  }
```

Notice also the `$util.escapeJavaScript()` calls in those templates to head off any attempt at injection attacks on those HTTP parameters.

[Method CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Method.html#)

[Method CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-method.html)

#### Lambda Functions

There are two Lambda function objects. They are both quite simple and both access our DynamoDB table. We pass the table name in as an environment variable.  The table name will end up as something quite unwieldy like 'acme-app-demo-AcmeAppDemoUserDataABCD4321-567890ZYXWVU' and is likely to change during your your development process.

We also pass in the permitted record types for each operation.  So for instance, users are allowed to read SUBSCRIPTION records but no create them. We expect SUBSCRIPTION records to be created when we receive a message from the payment service provider.

Notice we create an execution role for the two lambdas that gives them basic lambda execution permissions and the right to call 'PutItem' and 'Query' on our own Table object ... and nothing else. If you wanted to be super tight with your security model you could even break this in two so only the read lambda is allowed to Query and only the write lambda is allowed to PutItem.

[Lambda Function CDK docs](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html)

[Lambda Function CFN docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html)

## And Finally

You may notice there is no functionality in the test client for a user to create their own account. In tunasoniq.io we only create user accounts in the backend in response to receiving a subscription. You should find it easy enough to add end user onboarding if required.

There are bound to be things I have missed or could do better in the stack.  Feel free to get in touch with suggestions and/or hot-takes.

You can find me, mostly swearing about politics, on Twitter as @NoIAmTonyGreen.  You can also find me on [LinkedIn](https://www.linkedin.com/in/tony-green-8639616/).  Or you could even send a pull request.






