import boto3

class GetState:
    def __init__(self, region, instanceid):
        self.region = region
        self.instanceid = instanceid

    def get_state(self):
        ec2Client = boto3.client('ec2', region_name=self.region)
        instances = ec2Client.describe_instances(
            InstanceIds=[
                self.instanceid,
            ]
        )
        Instances = instances["Reservations"][0]
        state = Instances["Instances"][0]['State']['Name']

        return state
