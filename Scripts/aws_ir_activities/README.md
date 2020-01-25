# Cross-account IR activities
This script can be used by an IR Handler to create and analyse a snapshot located in another AWS account (referred to as the victim's AWS account).

# Pre-requisites
* IR Handler has provided an External ID to be used in the trust policy.
* The role ARN of the role set-up within the victim's AWS account is shared with the IR handler, to allow him/her to assume the role.
* Instance ID of the victim's EC2 instance.

# Execution steps
Basic instructions can be obtained by running:
`python3 aws_ir.py`

To obtain additional information about specific functionality (_create-role_, _grab-snapshot_ or _attach-volume-sift_), please run:
`python3 aws_ir.py grab-snapshot --help`

#### The following steps are to be run using the victim's AWS account
**create-role**: Create a role in the victim's AWS account to give the IR handler's AWS user account access to create an EC2 snapshot and modify its permission to allow for cross-account sharing of the snapshot.

`python3 aws_ir.py --profile PROFILE_NAME create-role 111111111111`


#### The following steps are to be run using the IR handler's AWS account
**grab-snapshot** : Snapshot the infected EC2 instance that is located in the victim's AWS account and give the Incident Handler's AWS account access to the created snapshot (_shows up under PrivateSnapshots in AWS_). Create a volume from this snapshot.

**attach-volume-sift**: Attach the volume of the infected EC2 to a SIFT machine in the IR Handler's AWS Account.

The created volume can be mounted in the SIFT instance using:
`sudo mount -o ro /dev/xvdh1 /mnt/`


# TODO
* Use KMS to encrypt and share the snapshot
* Obtain the region and availability zone, based on information provided in the aws config file

# Known Issues
* Does not obtain the region from the aws config file

#### References
* https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html
* https://n2ws.com/blog/how-to-guides/how-to-copy-encrypted-aws-snapshots
