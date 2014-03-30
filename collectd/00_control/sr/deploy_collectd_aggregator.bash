#!/bin/bash

##
PATH=/bin:/usr/bin:/sbin:/usr/sbin
SITE="unknown"
FP="/mnt/collectd/latest/configs"
SP="/etc"
FILE="collectd_server.conf"
FILE_NEW="collectd.conf"
RPMS="libcollectdclient-5.*.rpm collectd-5.*.rpm collectd-java-5.*.rpm collectd-snmp-5.*.rpm collectd-funnel-*.rpm"

release_check(){
        if [ -e /etc/redhat-release ]; then
                grep 'release 5' /etc/redhat-release 2>&1 > /dev/null
                if [ $? = 0 ]; then
                        echo "RHEL5.x host found"
                        OS=5
                fi
                grep 'release 6' /etc/redhat-release 2>&1 > /dev/null
                if [ $? = 0 ]; then
                        echo "RHEL6.x host found"
                        OS=6
                fi
        else
                OS=0
                echo "Not RedHat compatible... exiting"
                exit 1
        fi
}

check_mnt_mounted()
{
	#check if mnt is already mounted

	mount | grep "/mnt"
	if [ $? -eq 0 ];then
        	echo "[+] /mnt mounted already"
        	umount /mnt
        	if [ $? -eq 0 ];then echo "[+] Umount successful";else echo "[*] Failed";exit;fi
	fi
}

install_collectd()
{
        if [ $OS -eq 5 ]; then
            SITE=10.224.130.172
        elif [ $OS -eq 6 ]; then
            SITE=10.224.130.162
        else
            echo "Incompatible OS. Exiting."
            /bin/umount /mnt
            exit 1
        fi

	mount ${SITE}:/var/www/html/dev /mnt

	if [ $? -eq 0 ]; then
		echo "[+] Mount successful"
                echo "Deploying Packages"
                pushd /mnt/collectd/latest
                    yum -y install $RPMS
                popd
                
                echo "Copying Configuration"
		cp $FP/$FILE $SP/$FILE_NEW
		if [ $? -eq 0 ]; then
			echo "[+] file installed successfully";
		else
			echo "[*] Unable to install file";
		fi

                echo "Restarting Service"
                service collectd restart
		if [ $? -eq 0 ]; then
                    echo "Service restart successful"
                else 
                    echo "Unable to restart service"
                fi

	else
		umount /mnt
		echo "[*] failed to install";
		exit 1
	fi

        echo "Number of packages requested"
        echo $RPMS | wc -w

        echo "Number installed"
        rpm -qa | grep collectd | wc -l

        echo "Collectd packages installed (version)"
        rpm -qa | grep collectd

        echo "Timestamp of configuration"
        ls -al /etc/collectd.conf

	umount /mnt

       	if [ $? -eq 0 ];then echo "[+] Umount successful";else echo "[*] Failed";exit;fi
}

release_check
check_mnt_mounted
install_collectd
