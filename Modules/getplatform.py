import boto3

class GetInstancePlatform:
    def __init__(self, region, instanceid):
        self.region = region
        self.instanceid = instanceid

    def get_platform(self):
        ec2Client = boto3.client('ec2', region_name=self.region)
        instances = ec2Client.describe_instances(
            InstanceIds=[
                self.instanceid,
            ]
        )
        Instances = instances["Reservations"][0]
        # print(Instances)
        try:
            platform = Instances["Instances"][0]['Platform']
        except:
            platform = "Linux"
        # platform = Instances["Instances"][0]['Platform']
        return platform
