#! /usr/bin/env python
from boto.vpc import VPCConnection
from boto.ec2 import get_region, connect_to_region
import baker
import time

def create_vpc(region, vpc_cidr):
    ec2region = get_region(region)
    conn = VPCConnection(region=ec2region)
    return conn.create_vpc(vpc_cidr)

def create_internet_gateway(vpc):
    ec2region = vpc.region
    conn = VPCConnection(region=ec2region)
    return conn.create_internet_gateway()

def attach_internet_gateway(igw, vpc):
    ec2region = vpc.region
    conn = VPCConnection(region=ec2region)
    conn.attach_internet_gateway(igw.id, vpc.id)

def create_subnet(vpc, subnet_cidr):
    ec2region = vpc.region
    conn = VPCConnection(region=ec2region)
    return conn.create_subnet(vpc.id, subnet_cidr)

def create_route(vpc, target, gateway):
    ec2region = vpc.region
    conn = VPCConnection(region=ec2region)
    route_table = conn.get_all_route_tables(
        filters=[("vpc-id", vpc.id)])[0]
    conn.create_route(route_table.id, target, gateway_id=gateway.id)

def wait_for(instance):
    status = instance.update()
    while status == 'pending':
        time.sleep(10)
        status = instance.update()

EC2_REGION='ap-northeast-1'
VPC_CIDR='10.99.0.0/16'
PUBLIC_CIDR='10.99.0.0/24'
PRIVATE_CIDR='10.99.1.0/24'
DEFAULT_ROUTE='0.0.0.0/0'
KEY_NAME='your_name_here'
INSTANCE_TYPE='t1.micro'

@baker.command
def create_vpc_with_2_subnets(ec2_region=EC2_REGION,
                              vpc_cidr=VPC_CIDR,
                              public_cidr=PUBLIC_CIDR,
                              private_cidr=PRIVATE_CIDR,
                              default_route=DEFAULT_ROUTE):
    vpc = create_vpc(ec2_region, vpc_cidr)
    igw = create_internet_gateway(vpc)
    attach_internet_gateway(igw, vpc)
    subnet = create_subnet(vpc, public_cidr)
    subnet = create_subnet(vpc, private_cidr)
    create_route(vpc, default_route, igw)

@baker.command
def launch_instance(region=EC2_REGION,
                    subnet_id=None,
                    instance_type=INSTANCE_TYPE,
                    image_id=None,
                    key_name=KEY_NAME,
                    security_group_id=None):
    conn = connect_to_region(region)
    reserve = conn.run_instances(image_id=image_id,
                                 key_name=key_name,
                                 subnet_id=subnet_id,
                                 instance_type=instance_type,
                                 security_group_ids=[security_group_id])
    instance = reserve.instances[0]
    wait_for(instance)
    address = conn.allocate_address(domain="vpc")
    conn.associate_address(instance_id=instance.id,
                           public_ip=None,
                           allocation_id=address.allocation_id)


baker.run()