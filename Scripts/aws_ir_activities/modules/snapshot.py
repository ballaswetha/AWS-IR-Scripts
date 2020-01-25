# -*- coding: utf-8 *-*

""" Classes for creating a snapshot in victim's AWS account and giving IR handler's AWS account access """

import boto3
from botocore.exceptions import ClientError
import time

class Snapshot:

    def __init__(self, session, access_key_id, secret_access_key, session_token):
        """ Create snapshot object """
        self.session = session

        """ Set the session to use the temporary credentials provided by stsAssumeRole """
        self.ec2 = self.session.client(
            'ec2',
            aws_access_key_id = access_key_id,
            aws_secret_access_key = secret_access_key,
            aws_session_token = session_token
        )

    def create_snapshot(self, instance_id, ir_user_id):
        """ Create a snapshot of a specified EC2 instance in the victim AWS account """
        try:
            snapshot = self.ec2.create_snapshots(
                Description='EC2_Snapshot_IR',
                InstanceSpecification={
                    'InstanceId': instance_id
                }
            )

            while True:
                print("Snapshot creation in progress ...")
                time.sleep(10)
                snapshot_status = self.ec2.describe_snapshots(
                    SnapshotIds=[
                        snapshot['Snapshots'][0]['SnapshotId']
                    ]
                )
                if snapshot_status['Snapshots'][0]['State'] == 'completed':
                    break

            """ Modify snapshot permissions to give access to the IR Handler's account """
            try:
                response = self.ec2.modify_snapshot_attribute(
                    Attribute='createVolumePermission',
                    OperationType='add',
                    UserIds=[ir_user_id],
                    SnapshotId=snapshot['Snapshots'][0]['SnapshotId']
                )
            except ClientError as error:
                print(error.response['Error']['Message'])

            return snapshot
        except ClientError as error:
            print(error.response['Error']['Message'])
