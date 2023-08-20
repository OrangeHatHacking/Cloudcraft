import sys
import boto3

ec2 = boto3.client('ec2')

# TODO:
# add check for instant states before sending command
# 0: pending
# 16: running
# 32: shutting-down
# 48: terminated
# 64: stopping
# 80: stopped

def find_instance():
    response = ec2.describe_instances()['Reservations'][0]
    instances = response['Instances']
    for instance in instances:
        if instance['KeyName'] == 'minecraft':
            instance_id = instance['InstanceId']
            return instance_id
    sys.exit('Unable to find ec2 instance. Is there an ec2 instance with name "minecraft" available for this IAM user?\n')

def start_instance(instance_id):
    # Do a dryrun first to verify permissions
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    except Exception as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except Exception as e:
        print(e)

def stop_instance(instance_id):
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except Exception as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    err_string_not_recognised = "Invalid option: use -h or --help to show available options\n"
    err_string_num_args = "Too many arguments: use -h or --help to show available options\n"
    options = "usage: python3 serverController.py [option]\n\n\tstart \t(starts the ec2 instance)\n\tstop \t(stops the ec2 instance)\n"
    if len(sys.argv) > 2:
        sys.exit(err_string_num_args)
    elif len(sys.argv) < 2:
        sys.exit(err_string_not_recognised)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            sys.exit(options)
        elif sys.argv[1] == 'start':
            instance_id = find_instance()
            start_instance(instance_id)
        elif sys.argv[1] == 'stop':
            instance_id = find_instance()
            stop_instance(instance_id)
        else:
            sys.exit(err_string_not_recognised)

