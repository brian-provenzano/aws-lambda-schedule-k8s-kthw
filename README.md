# AWS Lambda Schedule Start / Stop of Instances (Quick / Dirty K8s,KTHW Usage)  
Contains a couple of quick and dirty lambda functions that in conjunction with CLoudWatch Event rules (scheduled) start/stop K8s instances that I created while playing around with Kubernetes The Hard Way.

AKA as save me some money on my personal AWSing...

## Overview
Contains a couple of quick and dirty lambda functions that in conjunction with CloudWatch Event rules (scheduled), start/stop K8s instances that I created while playing around with Kubernetes The Hard Way AWS version (my fork with scripts created as I type: [https://github.com/brian-provenzano/kubernetes-the-hard-way-aws](brian-provenzano/kubernetes-the-hard-way-aws))

## Components / Requirements
- `start-instances-k8s-kthw.py` - starts the instances tagged with tags with name:value = K8S:controller, K8S:worker
- `stop-instances-k8s-kthw.py` - stops the instances tagged with tags with name:value = K8S:controller, K8S:worker


## Usage
#### If you you are using this as-is for the same purpose I did (starting / stopping k8s labs for KTHW):

- Tag your controller instance with tag (name:value) = K8S:controller
- Tag your worker instances with tag (name:value) = K8S:worker


For example (or however you choose):

```
aws ec2 create-tags \
    --resources ${INSTANCE_ID} \
--tags "Key=K8S,Value=controller"
```


1. Create (2) Lambdas - using either your favorite IaC tool (Terraform,Cloudformation) or via the console
2. Create the (2) Cloudwatch event rules - again using IaC or manually.  Manual process is quickly detailed below (this may not be exact):
    - START schedule:
        - Cloudwatch -> events -> rules -> Create rule
        - Choose "Schedule", Cron expression - enter the schedule
        - Target -> Lambda function -> choose the function for "start-instances-k8s-kthw"
    - STOP schedule:
        - Cloudwatch -> events -> rules -> Create rule
        - Choose "Schedule", Cron expression - enter the schedule
        - Target -> Lambda function -> choose the function for "stop-instances-k8s-kthw"



#### If you just want to use this as a template / example on how to handle operational scheudling of instances:

1. Look at the code and adopt to your needs :)  Short and sweet...


## NOTES
- Use as you wish, there is nothing revolutionary here.  :)
- Also forgive the beginner look and feel of the functions - these were created when I was first starting with lambdas and for this specific purpose.  I just wanted to have these for posterity / examples in case I want ot revisit in the future.  These functions do not change the world...