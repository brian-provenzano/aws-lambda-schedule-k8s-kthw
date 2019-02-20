#
# TODO - change up to prevent blocking on each stop state; 
# may not be needed but keeping for now for graceful K8s shutdown
#
# First attempt at Lambda - forgive the slop
# 10.09.2018 - BJP
#

import boto3
# import logging

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
            'Values': ['running']
        }
    ]
    worker_filters = [{
            'Name': 'tag:K8S',
            'Values': ['worker']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    #filter the instances
    controller_instances = ec2.instances.filter(Filters=controller_filters)
    worker_instances = ec2.instances.filter(Filters=worker_filters)

    controllerid_running_instances = [instance.id for instance in controller_instances]
    workerid_running_instances = [instance.id for instance in worker_instances]
    
    #print the instances for logging purposes
    print("--Controller instances to stop: {0}".format(controllerid_running_instances))
    print("--Worker instances to stop: {0}".format(workerid_running_instances))
    
    # 1- Worker shutdown first
    if len(workerid_running_instances) > 0:
        instances = ec2.instances.filter(InstanceIds=workerid_running_instances)
        for instance in instances:
            instance.stop()
            print("-->Worker instance {0} STOPPING".format(instance.id))
            instance.wait_until_stopped()
            print("-->Worker instance {0} STOPPED".format(instance.id))
    else:
        print("-->No worker instances found to started - skipping...")
    
    # 2 -  Controller shutdown 
    if len(controllerid_running_instances) > 0:
        instances = ec2.instances.filter(InstanceIds=controllerid_running_instances)
        for instance in instances:
            instance.stop()
            print("-->Controller instance {0} STOPPING".format(instance.id))
            instance.wait_until_stopped()
            print("-->Controller instance {0} STOPPED".format(instance.id))
    else:
        print("-->No controller instances found to stop - skipping...")
    

    
