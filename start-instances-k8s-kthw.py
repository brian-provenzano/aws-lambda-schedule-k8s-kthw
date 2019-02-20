#
# TODO - change up to prevent blocking on each start state for workers - it is not needed
#
#
# First attempt at Lambda - forgive the slop
# 10.09.2018 - BJP
#

import boto3
#import logging

#setup simple logging for INFO
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    # Use the filter() method of the instances collection to retrieve
    # all running EC2 instances to deal with.
    controller_filters = [{
            'Name': 'tag:K8S',
            'Values': ['controller']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]
    worker_filters = [{
            'Name': 'tag:K8S',
            'Values': ['worker']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]
    
    #filter the instances
    controller_instances = ec2.instances.filter(Filters=controller_filters)
    worker_instances = ec2.instances.filter(Filters=worker_filters)

    controllerid_stopped_instances = [instance.id for instance in controller_instances]
    workerid_stopped_instances = [instance.id for instance in worker_instances]
    
    #print the instances for logging purposes
    print("--Controller instances to start: {0}".format(controllerid_stopped_instances))
    print("--Worker instances to start: {0}".format(workerid_stopped_instances))
    
    # 1 -  Controller start first 
    if len(controllerid_stopped_instances) > 0:
        instances = ec2.instances.filter(InstanceIds=controllerid_stopped_instances)
        for instance in instances:
            instance.start()
            print("-->Controller instance {0} STARTING".format(instance.id))
            instance.wait_until_running()
            print("-->Controller instance {0} STARTED".format(instance.id))
    else:
        print("-->No controller instances found to start - skipping...")
    
    
    # 2 - Worker start
    if len(workerid_stopped_instances) > 0:
        instances = ec2.instances.filter(InstanceIds=workerid_stopped_instances)
        for instance in instances:
            instance.start()
            print("-->Worker instance {0} STARTING".format(instance.id))
            instance.wait_until_running()
            print("-->Worker instance {0} STARTED".format(instance.id))
    else:
        print("-->No worker instances found to start - skipping...")
    