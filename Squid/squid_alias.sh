
echo '------------------------------------------------------------------------------start_squid_alias'

scp ./bashrc_alias.sh root@192.168.31.2:bashrc_alias.sh

echo '------------------------------------------------------------------------------doing_chmod'

ssh root@192.168.31.2 -t 'chmod 755 /root/bashrc_alias.sh'

echo '------------------------------------------------------------------------------doing_ln_sf'

ssh root@192.168.31.2 -t 'ln -sf /root/bashrc_alias.sh /bin/squid_alias'
ssh root@192.168.31.2 -t 'squid_alias'

echo '------------------------------------------------------------------------------end_squid_alias'
