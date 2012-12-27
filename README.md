aws-scripts
===========

AWS Auto generator scripts

Initial Settings
```
https://gist.github.com/4242303
https://gist.github.com/4242484
https://gist.github.com/4230004


$ workon bootcamp

export AWS_ACCESS_KEY_ID=xxxx
export AWS_SECRET_ACCESS_KEY=xxxx

python vpc.py create_vpc_with_2_subnets \
--ec2_region=ap-northeast-1 \
--vpc_cidr=10.88.0.0/16 \
--public_cidr=10.88.0.0/24 \
--private_cidr=10.88.1.0/24 \
--default_route=0.0.0.0/0 \


python vpc.py launch_instance \
--image_id=ami-4e6cd34f \
--subnet_id=subnet-4726622e \
--security_group_id=sg-d9a0bcb5 \
--region=ap-northeast-1 \
--key_name=khkey \
--instance_type=t1.micro


[fabric]
https://gist.github.com/4242247

fab -c rcfile -H 10.0.0.91 deploy

fab -f fabfile/fabfile.py -c fabfile/rcfile -H 10.0.0.91 deploy
http://xxxx/wordpress/

fab -f fabfile/fabfile_jenkins.py -c fabfile/rcfile -H 10.0.0.91 deploy
http://xxxx:8080
```