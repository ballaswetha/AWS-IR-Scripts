# Incident Response for AWS

A collection of scripts to help IR handlers automate some of the tasks required for analysis. 

* Create a SIFT AMI image 
* AWS IR functions:
** Create a role that allows cross-account access use with an External ID
** Create a snapshot of an EC2 instance and give the IR Handler's account permission to access the snapshot
** Attach a volume to a SIFT machine for dead box forensics 

#### High-level AWS architecture (focus on security) 
![alt text](https://github.com/ballaswetha/AWS/raw/master/ArchDiagrams/Dec%202019%20AWS%20Services.png "High-level AWS service architecture")

Link to lucidchart diagram: https://www.lucidchart.com/documents/edit/e62bc6ee-b8ee-4a34-ac12-0245bd08a6bf 

#### References
* https://d1.awsstatic.com/whitepapers/aws_security_incident_response.pdf 
