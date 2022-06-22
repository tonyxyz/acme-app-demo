# acme-app-demo

This repo provides a demonstration app that may be useful as a bootstrap backend for some kinds of online enterprises.  It is an AWS based stack consisting of API Gateway, some Lambdas, a Cognito User Pool and DynamoDB Table. The code here has largely been lifted from tunasoniq.io (“the learning music app”) at a certain point in time - which I can do because tunasoniq belongs to me.  Tunasoniq’s own code base is proprietary and Acme App Demo is MIT licensed, there is no ongoing dependency between the two.

Acme App Demo is Python-centric. It uses Cloud Development Kit (CDK) code in Python and the Lambdas are also in Python.  CDK code can also be written in TypeScript, JavaScript, Java, C#/.Net or GoLang if those languages are more suitable for your organisation.  You can also write Lambdas in all of those languages as well as PowerShell.

There are various ways of getting an enterprise-grade backend off the ground: there probably are still people out there building LAMP stack applications, there are certainly still new-build Ruby on Rails, Firebase and Spring Boot applications.

Building a new application on AWS is appealing for a lot of reasons (which I’m not going to go into here) but getting to the starting line with AWS can be a big ask for small startups teams especially if their main focus is on delivering front-end experience.

AWS have a solution for this - it’s called Amplify.  Amplify gets a lot of traction and a lot of serious businesses have been built on it but - cards on table - I do not like Amplify.  Amplify is a highly opinionated framework and, as with your Brexit voting uncle, it is often difficult to understand why it holds those opinions.  I have seen businesses, who probably should have known better, going a long way down the wrong path because of decisions taken for them by Amplify.  Amplify is also full of secret spider glue: there are parts of an Amplify app that are strangely opaque and painful to refactor when your startup moves up to a bigger league.

On the other hand it ought to be easy, with a little bit of effort, to build an app like an Amplify app but with a more transparent tool set.  AWS’s main tool for wrangling cloud stacks is CloudFormation (CFN) which uses JSON or YAML configuration files to build your stack. More recently the AWS developer community has embraced CloudDeveloperKit (CDK). CDK allows you to write configuration-as-code in several popular languages. CDK generates and manages CFN files on your behalf.  If you need to move away from CDK you can simply extract the CFN files to create a clean break.

The CDK code is going to be terser than the corresponding CFN and is likely to be more malleable - if you need to make changes, especially if you need to make far-reaching changes, it will be easier in CDK than raw CFN.

However, it turns out it really is not easy, starting from scratch to build a CDK app that delivers the same features as a simple Amplify app mainly because there just are a lot of wrinkles and pitfalls in slotting the AWS components together.  Not all of those wrinkles and pitfalls are clearly documented and, because AWS tries really hard to be an open platform with lots of languages and tools and approaches, even when things are documented it can be a challenge to find just the nugget you need.

So that is why Acme App Demo is here. It creates a stack with four main components:

  - user authentication with a Cognito User Pool
  - an API Gateway for users, with an OAuth authorizer
  - a couple of Lambdas accessed via the API Gateway
  - a user data store in the form of a DynamoDB table.

There is also a smoke test which will create a test user and then launch a demo web page which allows you to exercise most of the deployed code.

Not everything here is 100% ready for production. I’ve tried to point out areas where you may want to further lock down and configure the code before releasing it into the wild. But I hope it gets you to within sight of the starting line relatively quickly.

## Requirements
#### Clone the Repo
```
cd your-work-directory
git clone https://github.com/tonyxyz/acme-app-demo.git
cd acme-app-demo
```
#### AWS
If you are not yet set up with an AWS account read their own [getting started](https://aws.amazon.com/getting-started/) guide. You should set up a user within your AWS account who has permissions to create and run CDK apps and make this user your default user. The usual way to do this is to edit ` ~/.aws/credentials`.

If you work through the setup tutorials in the AWS link above you will have this.

If you have a new account that qualifies for the free tier you can probably setup and test Acme App Demo for free, if not it will maybe cost you a few pennies.

Of course, when you have millions of users and terabytes of application data it will cost you a lot more but, by that stage, you will have many interesting problems.

#### NodeJS
NodeJS is required by the core CDK cli app. The smoke test web page does not require NodeJS to build.

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

Of course, if you are building a web client in another project it would make sense to do it there.

#### Python

The latest version of Python currently supported in AWS Lambda (at the time of writing) is 3.9 so it makes sense to set up a virtual environment using 3.9 to contain the project dependencies. If your local python is based on pyenv do something like this:

```
pyenv install --list
pyenv install 3.9.12
pyenv global 3.9.12
python --version
```
Or, if you are an opinionated python developer, do something else.

When you create a Python CDK project  from scratch using
```
cdk init app --language=python
```
CDK will create a venv virtual environment for you in .venv/ . You can do the same here using
```
python3 -m venv .venv
```
Or if you currently use pyenv-virtualenv or conda for managing virtual environments these will probably work equally well.

