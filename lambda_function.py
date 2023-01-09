import boto3

REGION = ''
INSTANCES = ['']
USERNAME = ''
INSTANCE_KEYPAIR = ''

def get_ec2_ipv4():
    '''
    Retrieve the dynamic public IP of the instance/s once online
    '''
    
    main_key = 0
    filters = [{  
        'Name': 'instance-id',
        'Values': INSTANCES
    }]
    instance_props = {
        'instance_id': '',
        'ipv4':''
    }
    return_instances = []

    try:
        ec2_client = boto3.client('ec2')
        instances = ec2_client.describe_instances(Filters=filters)

        if instances and ('Instances' in instances['Reservations'][main_key].keys()):
            for r in instances['Reservations']:
                for inst in r['Instances']:
                    if( 'PublicIpAddress' in inst.keys()):
                        return inst['PublicIpAddress']
                        # instance_props['instance_id'] = inst[''] ## Needs testing
                        instance_props['ipv4'] = inst['PublicIpAddress']
                        return_instances.append(instance_props)
    except Exception as e:
        print (e.args)
                    
    return return_instances


def lambda_handler(event, context):
    print (f'event {event}, \n\ncontext {context}')
    print(f'<<<<<<Lambda Exec Start>>>>>>')

    instances = []
    try:
        ## Get the IPV4s of the ec2 instances
        instances = get_ec2_ipv4()
        print(f'Instances retrieved: {instances}')
        
    except Exception as e:
        print (e.args)
    
    print(f'------Lambda Exec End------')

    return{ 'statusCode': 200 }