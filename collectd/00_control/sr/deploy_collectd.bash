#!/bin/bash

##
PATH=/bin:/usr/bin:/sbin:/usr/sbin
#SITE=$( hostname | cut -d- -f4 | sed PMS="libcollectdclient-5.3.1*.rpm collectd-5.3.1*.rpm collectd-curl-5.3.1*.rpm collectd-curl_json-5.3.1*.rpm collectd-curl_xml-5.3.1*.rpm collectd-snmp-5.3.1*.rpm"
SITE=build62
FP="/mnt/collectd/latest/configs"
SP="/etc"
FILE="collectd_server.conf"
FILE_NEW="collectd.conf"
RPMS="libcollectdclient-5.*.rpm collectd-5.*.rpm"

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
	mount ${SITE}:/var/www/html/rhel6_dev /mnt
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

check_mnt_mounted
install_collectd
