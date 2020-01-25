""" Classes for assuming a role in another AWS account, using an external ID and role ARN """

import boto3
import subprocess
from botocore.exceptions import ClientError

class ModifySecurityGroup:

    def __init__(self, session):
        """ Create a ModifySecurityGroup object """
        self.session = session
        self.ec2 = self.session.client('ec2')

    def change_security_group_rules(self, instance_id, ir_security_group_id): #TODO - Doesn't seem to find the instance ID!
        """ Modify the security group associated with the infected instance to only traffic from a security group assigned to the Incident Handler """

        """ Get the security group ID associated with the infected instance """
        response = self.ec2.describe_hosts()
        print(response)
        try:
            instance_details = self.ec2.describe_instance_attribute(Attribute='groupSet', InstanceId=instance_id)
            print(instance_details)
        except ClientError as error:
            print(error.response['Error']['Message'])

        
