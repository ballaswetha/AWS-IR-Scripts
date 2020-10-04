#! /usr/bin/python
# -*- coding: utf-8 *-*

import boto3
import click
import random 
import string
import os
__path__=[os.path.dirname(os.path.abspath(__file__))]
import subprocess
from aws_ir.modules.snapshot import Snapshot
from aws_ir.modules.externalid_policy import ExternalIdPolicy
from aws_ir.modules.assume_role_arn import AssumeRoleARN
from aws_ir.modules.modify_security_group import ModifySecurityGroup

session = None
snapshot = None
externalid_policy = None
assume_role_arn = None
modify_security_group = None

@click.group()
@click.option('--profile', default=None, help="Provide the name of the required AWS profile")
def cli(profile):
    global session, client, snapshot, externalid_policy, assume_role_arn, modify_security_group

    session_cfg={}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg, region_name='us-east-1') #TODO - doesn't seem to pick-up region from the config file

@cli.command('create-role')
@click.argument('ir_account_id')
# @click.argument('external_id')
def create_role_arn(ir_account_id):
    """ Create a role in the victim's AWS account """
    external_id=''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    externalid_policy = ExternalIdPolicy(session)
    ir_role = externalid_policy.create_role(ir_account_id, external_id) # TODO - print role arn, default session duration is 1 hour - does this need to be higher?
    # print("Role ARN details to be provided to the IR Handler: ", ir_role['Role']['Arn'])
    # print(ir_role, "\n\n\n")
    print(ir_role)

@cli.command('grab-snapshot')
@click.argument('instance_id')
@click.argument('role_arn')
@click.argument('external_id')
@click.argument('ir_user_id')
def grab_snapshot(instance_id, role_arn, external_id, ir_user_id):
    """ Create a snapshot of the victim machine """
    assume_role_arn = AssumeRoleARN(session)
    """ Assume the role in the victim's AWS account to snapshot the victim EC2 instance """
    assume_role = assume_role_arn.assume_role_arn(role_arn, external_id)

    """ Grab a snapshot of the victim's EC2 machine. """
    snapshot = Snapshot(session, assume_role['Credentials']['AccessKeyId'], assume_role['Credentials']['SecretAccessKey'], assume_role['Credentials']['SessionToken'])
    victim_instance = snapshot.create_snapshot(instance_id, ir_user_id)

    """ Create a volume in IR Handler's AWS account to be analysed """
    ec2 = session.client('ec2')
    try:
        volume = ec2.create_volume(
            AvailabilityZone = 'us-east-1a', #TODO - take from profile??
            SnapshotId = victim_instance['Snapshots'][0]['SnapshotId']
        )
        print("Volume ID: ", volume['VolumeId'])
    except ClientError as error:
        if error.response['Error']['Code'] == 'IncorrectState':
            print(error.response['Error']['Message'])
        else:
            raise error

@cli.command('attach-volume-sift')
@click.argument('sift_instance_id')
@click.argument('volume_id')
def attach_volume_sift(sift_instance_id, volume_id):
    """ Attach the victim's volume to a SIFT EC2 """
    ec2 = session.resource('ec2')
    sift_instance = ec2.Instance(sift_instance_id)
    response = sift_instance.attach_volume(
        Device = '/dev/sdh', #TODO - maybe this can be an argument?
        VolumeId = volume_id
    )

@cli.command('create-security-group')
@click.argument('instance_id')
def create_security_group(instance_id):
    """ Create a security group to be attached to the SIFT instance """
    #TODO

@cli.command('modify-security-group')
@click.argument('instance_id')
@click.argument('ir_security_group_id')
def modify_security_group(instance_id, ir_security_group_id):
    """ Modify the ingress and egress rules for the security group to allow communication only with the IR Handler's security group """

    modify_security_group = ModifySecurityGroup(session)
    reponse = modify_security_group.change_security_group_rules(instance_id, ir_security_group_id)
    #ir_role = externalid_policy.create_role(ir_account_id, external_id) 


if __name__ == '__main__':
    cli()
