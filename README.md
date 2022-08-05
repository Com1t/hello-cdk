## hello-cdk

This repository will introduce you how take [Serverless scikit-learn Model Serving](https://github.com/aws-samples/aws-lambda-docker-serverless-inference/tree/main/scikit-learn-inference-docker-lambda) lambda fucntion to work with AWS cdk
In this tutorial, I'm going to introduce how to use lambda function with cdk, while using docker environment

The reason why we use docker environment, instead of simple `layer + source code` is beacuse AWS limits only 250MB for layers, which is very limited for us as data scientist that we use big library all the time

See some more information about limited layer size [Building layer for nft model](https://hackmd.io/ammHmkPuQ-uTpw-uf2tM9A)

## Steps for creating docker version of lambda
Here I'm going to take [aws-lambda-docker-serverless-inference/scikit-learn-inference-docker-lambda](https://github.com/aws-samples/aws-lambda-docker-serverless-inference/tree/main/scikit-learn-inference-docker-lambda) as a example, to introduce how to use lambda function with docker

### Create your own docker file
After you prepared your lambda handler
Your question would be how to use docker to build the environment
It's very easy to build a dockerfile for lambda
AWS provide most runtime that we mostly use, they also give you the right to choose some other docker images as you want
[See here for more information](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-images.html#runtimes-images-lp)
All you need to do is to choose the right runtime, build dependencies, and set `CMD` to your lambda handler
```
FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt ./
RUN python3.7 -m pip install -r requirements.txt -t .

COPY ./train-code/scikit_learn_iris.py ./
RUN python scikit_learn_iris.py

COPY ./app/app.py   ./

CMD ["app.handler"]
```
And build a 'yaml' file to tell 'sam' how to build this image properly(e.g. where's the `Dockerfile`), and set it's name for invoke (Here the name is set as 'ScikitLearnInferenceFunction')
```
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: >
  scikit-learn-inference-docker-lambda
  SAM Template for scikit-learn-inference-docker-lambda
Resources:
  ScikitLearnInferenceFunction:
    Type: AWS::Serverless::Function # More info about Function Resource: https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md#awsserverlessfunction
    Properties:
      PackageType: Image
      MemorySize: 256
      Timeout: 60
    Metadata:
      DockerTag: python3.7-v1
      DockerContext: .
      Dockerfile: Dockerfile

Outputs:
  ScikitLearnInferenceFunction:
    Description: "ScikitLearnInference Lambda Function ARN"
    Value: !GetAtt ScikitLearnInferenceFunction.Arn
  ScikitLearnInferenceFunctionIamRole:
    Description: "Implicit IAM Role created for ScikitLearnInference function"
    Value: !GetAtt ScikitLearnInferenceFunction.Arn
```
Then use `sam build` to build this image
And use `sam local invoke {function name} --event {event for lambda}.json` to test lambda function correctness

### Create a cdk environment
Create the cdk environment in any empty folder by
`cdk init --language python`

Yout should see 'cdk' provides following files for you
![](https://i.imgur.com/Niotde4.png)

The most important parts are 'cdk.json' and 'app.py'

In 'cdk.json' you will tell 'cdk' where is the entrypoint of your instruction for IaC, and what file should be include or not

![](https://i.imgur.com/Ef1BcL2.png)

In 'app.py' you will tell 'cdk' AWS deployment information
Here, I create a class inheritant 'Stack'
In line 18-22, I use 'DockerImageFunction' constructor of 'aws_lambda' to indicate what type of our function shuold be and where are the contents needed for buildiing phase(line 19)
The rest are just for building the entire thing up, which is identical to normal lambda
![](https://i.imgur.com/xFZBDv5.png)

After all these been done,
we can use 'cdk synth' to check everything is working
and use 'cdk deploy' to deploy this function

### Good to go
Finally, you should be able to create a lambda function
![](https://i.imgur.com/3awnol7.png)

And, test whether it works properly
![](https://i.imgur.com/whgG1Jv.png)
