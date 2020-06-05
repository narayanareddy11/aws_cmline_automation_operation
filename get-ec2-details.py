import boto3
from Modules.getregion import GetRegion
from Modules.getplatform import GetInstancePlatform
from Modules.getreservation import GetBillingOpt
from Modules.getstate import GetState
from Modules.getinstancetype import GetInstanceType
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
        get_platform = GetInstancePlatform(region, inst)
        # Getting Billing type of the instance in the region
        get_reserve = GetBillingOpt(region, inst)
        # Getting Instance Type of the instance in the region
        get_type = GetInstanceType(region, inst)

        status = get_status.get_state()
        platform = get_platform.get_platform()
        reservation = get_reserve.get_bill_details()
        type = get_type.get_instance_type()

        Details = [status, platform, type, reservation]

        InstMetadata[inst] = Details
        InstDetails.append(InstMetadata)
    Metadata[region] = InstDetails

# Writing the output in a CSV File
print(Metadata)
datenow = datetime.now()
date = datenow.strftime("%d-%B-%Y-%H-%M")
CSVFile = "C:\\Users\\arnabnandy1\\Documents\\Codes\\AwsMetadata\\CSV\\csv_outputs\\ec2_status_output_" + date + ".csv"
# CSVFile = "/Users/arnabnandy/PycharmProjects/aws_metadata/CSV/csv_outputs/ec2_status_output_"+ date + ".csv"

with open(CSVFile, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Region", "InstanceID", "Status", "Platform", "InstanceType", "Bill Type"])

for regions in Metadata.keys():
    for details in Metadata[regions]:
        print(details)
        for ins_id in details.keys():
            status = details[ins_id][0]
            Platform = details[ins_id][1]
            type = details[ins_id][2]
            BILL = details[ins_id][3]

            print(regions, ins_id, status, Platform, type, BILL)
            try:
                with open(CSVFile, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [regions, ins_id, status, Platform, type, BILL])
            except TypeError:
                with open(CSVFile, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        ["NA","NA","NA","NA","NA","NA"])
