from fabric.api import run, env, sudo
from fabric.context_managers import cd


def check():
    for k in env:
        print k, env[k]

def install_httpd():
    sudo("yum -y install httpd")
    sudo("chkconfig httpd on")
    sudo("service httpd start")
    
def install_php():
    sudo("yum -y install php php-mysql")
    sudo("service httpd restart")
         
def install_mysql_server():
    sudo("yum -y install mysql-server")
    sudo("chkconfig mysqld on")
    sudo("service mysqld start")

def setup_mysql_server():
    run("mysqladmin -uroot password %(mysql_root_password)s" % env)
    
def setup_wp_database():
    run("mysql -uroot -p%(mysql_root_password)s -Bse 'CREATE DATABASE IF NOT EXISTS %(wp_database)s CHARACTER SET utf8 COLLATE utf8_general_ci;'" % env)
    run("mysql -uroot -p%(mysql_root_password)s -Bse 'GRANT ALL PRIVILEGES ON %(wp_database)s.* TO %(wp_dbuser)s@\"localhost\" IDENTIFIED BY \"%(wp_dbpassword)s\"';" % env)

def install_wordpress():
    with cd('/var/www/html'):
        sudo("wget http://wordpress.org/latest.tar.gz")
        sudo("tar -xzvf latest.tar.gz")

def setup_wordpress():
    with cd('/var/www/html/wordpress'):
        sudo("sed -e s/database_name_here/%(wp_database)s/ -e s/username_here/%(wp_dbuser)s/ -e s/password_here/%(wp_dbpassword)s/ wp-config-sample.php > wp-config.php" % env)

def deploy():
    install_httpd()
    install_php()
    install_mysql_server()
    setup_mysql_server()
    setup_wp_database()
    install_wordpress()
    setup_wordpress()