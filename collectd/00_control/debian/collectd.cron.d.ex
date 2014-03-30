#
# Regular cron jobs for the collectd package
#
0 4	* * *	root	[ -x /usr/bin/collectd_maintenance ] && /usr/bin/collectd_maintenance
