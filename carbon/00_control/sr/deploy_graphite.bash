#!/bin/bash

##
PATH=/bin:/usr/bin:/sbin:/usr/sbin
#SITE=$( hostname | cut -d- -f4 | sed PMS=""
SITE=build62
FP="/mnt/latest/configs"
SP="/etc"
FILE=""
FILE_NEW=""
RPMS="graphite-web*.rpm"

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

install_graphite()
{
	mount ${SITE}:/var/www/html/rhel6_dev /mnt
	if [ $? -eq 0 ]; then
		echo "[+] Mount successful"
                echo "Deploying Packages"
                pushd /mnt/latest
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
                service httpd restart
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
        rpm -qa | grep graphite | wc -l

        echo "Collectd packages installed (version)"
        rpm -qa | grep graphite

        echo "Timestamp of configuration"

	umount /mnt

       	if [ $? -eq 0 ];then echo "[+] Umount successful";else echo "[*] Failed";exit;fi
}

check_mnt_mounted
install_graphite
