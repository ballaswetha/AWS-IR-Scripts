""" Classes for assuming a role in another AWS account, using an external ID and role ARN """

import boto3
import subprocess
from botocore.exceptions import ClientError

class AssumeRoleARN:

    def __init__(self, session):
        """ Create an assume_role object """
        self.session = session
        self.sts = self.session.client('sts')

    def assume_role_arn(self, role_arn, external_id):
        """ Assume role using STS and ExternalID to avoid the confused deputy problem """
        try:
            assume_role = self.sts.assume_role(
                RoleArn = role_arn,
                RoleSessionName = 'IR_Handler_Assume_Role',
                ExternalId = external_id
            )

            return assume_role
        except ClientError as error:
            print(error.response['Error']['Message'])
