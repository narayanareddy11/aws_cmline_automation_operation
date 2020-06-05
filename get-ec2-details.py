import boto3
from Modules.getstate import GetState

from datetime import datetime
import csv

get_regions = GetRegion()
# Getting all the region
Regions = get_regions.get_regions()
RegionInstance = {}
for r in Regions:
    # Getting all the instances in that particular region
    ec2Client = boto3.client('ec2', region_name=r)
    instances = ec2Client.describe_instances()
    try:
        Instances = instances["Reservations"]
        InstanceList = []
        for ins in Instances:
            InsID = ins["Instances"][0]['InstanceId']
            InstanceList.append(InsID)
            print(InsID)
    except IndexError:
        print(r + ",No Instances")
    RegionInstance[r] = InstanceList

Metadata = {}

for region in RegionInstance.keys():
    InstDetails = []
    for inst in RegionInstance[region]:
        InstMetadata = {}
        Details = []
        # Getting Status of the Instance
        get_status = GetState(region, inst)
        # Getting OS of the instance in the region

        status = get_status.get_state()
        Details = [status, platform, type, reservation]
        InstMetadata[inst] = Details
        InstDetails.append(InstMetadata)
    Metadata[region] = InstDetails

# Writing the output in a CSV File
print(Metadata)
datenow = datetime.now()
date = datenow.strftime("%d-%B-%Y-%H-%M")



