# Overview
Build a SIFT instance (AWS soft instance type) on Ubuntu 18.04, using SIFT CLI. The build was tested with a couple of test cases (Hacking Case and Data Leakage Case in the CFReDS project and the forensicate.cloud workshop) - to ensure that there are no known problems. 

The `default` profile configured in AWS is used for building the image. 

# Pre-requisites
- Install packer.
- Reference: https://www.packer.io/intro/getting-started/install.html

# Execute steps
### AMI Creation with Packer
```
cd packer
packer validate sift_packer-template.json
packer build sift_packer-template.json
```

# TODO
- Provide flexibility to automate image creation with AWS Code Build and CodePipeline
- Provide the ability to use different AWS profiles for creatiion of the SIFT instance

# References
* https://github.com/teamdfir/sift-cli
* https://www.cfreds.nist.gov/ 
* https://forensicate.cloud/ws1/ 