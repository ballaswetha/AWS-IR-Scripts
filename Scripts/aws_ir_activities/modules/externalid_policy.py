# -*- coding: utf-8 -*-

""" Classes for creating a role in the victim's AWS account for the IR Handler's AWS account to create a snapshot of the victim's machine """

import boto3
import json
from botocore.exceptions import ClientError

class ExternalIdPolicy:

    def __init__(self, session):
        """ Create ExternalIdPolicy object """
        self.session = session
        self.iam = self.session.client('iam')

    def create_role(self, ir_account_id, external_id):
        ir_role_name = "IRHandlerAccessRole"
        """ Create a role that allows the IR Handler access to specified actions """

        """ Create the policy that will be attached to the role """
        try:
            ir_managed_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "IRHandler",
                        "Effect": "Allow",
                        "Action": [
                            "ec2:ModifySnapshotAttribute",
                            "ec2:DescribeSnapshots",
                            "ec2:CreateSnapshots"
                        ],
                        "Resource": [
                            "arn:aws:ec2:*:*:instance/*",
                            "arn:aws:ec2:*::snapshot/*",
                            "arn:aws:ec2:*:*:volume/*"
                        ]
                    }
                ]
            }
            """ Create the role and attach the policy created above """
            ir_trust_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": ir_account_id
                        },
                        "Action": "sts:AssumeRole",
                        "Condition": {
                            "StringEquals": {
                                "sts:ExternalId": external_id
                            }
                        }
                    }
                ]
            }
            """ Create the role and attach the policy created above """
            ir_role = self.iam.create_role(
                RoleName=ir_role_name,
                Description="Provide the IR Handler's AWS account access to specified AWS actions",
                AssumeRolePolicyDocument=json.dumps(ir_trust_policy)
            )
            """ Wait till IAM role is created """
            iam_waiter = self.iam.get_waiter('role_exists')
            iam_waiter.wait(
                RoleName=ir_role_name,
                WaiterConfig={
                    'Delay' : 10,
                    'MaxAttempts' : 12
                }
            )
            """ Attach the policy created above to the role """
            response = self.iam.put_role_policy(
                RoleName='IRHandlerAccessRole',
                PolicyDocument=json.dumps(ir_managed_policy),
                PolicyName='IRHandlerAccessPolicy'
            )
            create_role_message = "Provide the following Details to IR handler: " + "\n" + \
                "Role ARN: " + ir_role['Role']['Arn'] + "\n" + "External ID: " + external_id
            return create_role_message
        except ClientError as error:
            return error.response['Error']['Message']

        
