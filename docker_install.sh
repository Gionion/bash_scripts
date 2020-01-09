#!/bin/bash

set -e

DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PARENT_DIR=$(dirname $DIR)
PYTHON="python3 $DIR/compose.py"
COMPOSE_VERSION=$($PYTHON --parameter compose)
#RPM=$($PYTHON --parameter rpm)
#OS=$($PYTHON --parameter os)
#GPG=$($PYTHON --parameter gpg)

function install_docker(){
	
	function install_compose(){		
		
		curl -L https://github.com/docker/compose/releases/download/$COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
		chmod +x /usr/local/bin/docker-compose

		if grep -q "docker" /etc/group; then
			:
		else
			groupadd docker
		fi

		usermod -aG docker $USER
	}

	function docker_enterprise(){
		rm /etc/yum.repos.d/docker*.repo
		read -e -p "Insert your Docker-EE-URL: " DOCKERURL
		export $DOCKERURL
		sudo -E sh -c 'echo "$DOCKERURL/rhel" > /etc/yum/vars/dockerurl'
		RHEL_Version=$(cat /etc/redhat-release | awk '{print $7}')
		sh -c 'echo "$RhVersion" > /etc/yum/vars/dockerosversion'
		yum install -y yum-utils device-mapper-persistent-data 
		yum-config-manager --enable rhel-7-server-extras-rpms

		read -e -p "Is this machine running on AWS or Azure? AWS, Azure, None of them [press 'ENTER']" Cloud
		case $Cloud in
			"AWS")
				yum-config-manager --enable rhui-REGION-rhel-server-extras
			;;
			"Azure")
				yum-config-manager --enable rhui-rhel-7-server-rhui-extras-rpms

				if $? -ne 0; then
					yum-config-manager --enable rhui-rhel-$RHEL_Version-server-rhui-extras-rpms
				fi
			;;
			*)
				:
			;;
		esac
		
		sudo -E yum-config-manager --add-repo "$DOCKERURL/rhel/docker-ee.repo"
		yum -y install docker-ee

		if $? -ne 0; then
			yum-config-manager --enable rhel-$RHEL_VERSION-server-extras-rpms								
		fi

		install_compose
		
		if [ -x "$(command -v unzip)" > /dev/null ]; then
			:
		else
			yum install -y unzip
		fi
	}

	function centos_redhat2(){		
		cat > "/etc/yum.repos.d/centos.repo" <<EOF
[centos]
name=centos
baseurl=$OS
enabled=1
gpgcheck=1
gpgkey=$GPG
EOF
		sudo yum install -y $RPM
		#curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
		#pip install docker-compose
		install_compose
	}

	function centos_redhat(){		
		yum install -y yum-utils device-mapper-persistent-data lvm2
		yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
		yum install -y docker-ce

		install_compose
	}

	function debian_like(){
		if [ $OS_NAME == "ubuntu" ]; then
			apt install -y apt-transport-https ca-certificates curl software-properties-common
			curl -fsSL https://download.docker.com/linux/$OS_NAME/gpg | apt-key add -
			add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable"
		elif [ $OS_NAME == "debian" ]; then
			apt install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
			curl -fsSL https://download.docker.com/linux/$OS_NAME/gpg | apt-key add -
			add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
		fi
	}
	#end of definitions
	#main program start
	function main(){
		case $OS_NAME in
			"ubuntu"|"debian")
				debian_like	
				apt -y update
				apt -y upgrade
				apt install -y docker-ce

				if [ -x "$(command -v unzip)" > /dev/null ]; then
					:
				else
					apt install -y unzip
				fi

				install_compose
			;;
			"\"centos\"")
				yum install -y yum-utils device-mapper-persistent-data lvm2
				yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
				yum install -y docker-ce
				
				if [ -x "$(command -v unzip)" > /dev/null ]; then
					:
				else
					yum install -y unzip
				fi			
			;;
			"\"rhel\"")
				read -e -p "There's not DockerCE for redhat, do you want to install the Enterprise Edition? Yes[y], No[n]" $rhel
				case $rhel in
					y|Y)
						docker_enterprise
					;;
					n|N)
						read -e -p "Do you want to install Docker CE using Centos repositories? Yes[y], No[N]" $centos_repo
						case $centos_repo in
							y|Y )
								centos_redhat
							;;
							*)
								exit 0
							;;
						esac
					;;
					*)
						exit 0
					;;
				esac
			;;
		esac
	}
	main
}

if [ $EUID -ne 0 ]; then
	echo "You must run this as root"
	exit 0
else
	if [ -x "$(command -v docker)" > /dev/null ]; then
		echo "docker is already installed in this machine"
	else
		OS_NAME=$(grep -w ID /etc/os-release | cut -d '=' -f2)
		install_docker $OS_NAME
	fi
fi

