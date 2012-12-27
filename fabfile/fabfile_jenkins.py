from fabric.api import run, env, sudo
from fabric.context_managers import cd


def check():
    for k in env:
        print k, env[k]

def install_jenkins():
        sudo("wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo")
        sudo("rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key")
        sudo("yum install -y jenkins")

def setup_jenkins():
        sudo("service jenkins start")


def deploy():
    install_jenkins()
    setup_jenkins()