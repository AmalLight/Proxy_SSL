
echo '------------------------------------------------------------------------------start_bashrc_alias'

bashrc_content=`cat /root/.bashrc`

echo '------------------------------------------------------------------------------read_bashrc'

echo '------------------------------------------------------------------------------start_ifthen'

if [[ $bashrc_content != *squid_alias* ]] ; then
    
    echo '------------------------------------------------------------------------------inside_ifthen'

    echo ''               >> /root/.bashrc
    echo '# squid_alias'  >> /root/.bashrc

    echo "alias rmi='rm -i'"  >> /root/.bashrc
    echo "alias cpi='cp -i'"  >> /root/.bashrc
    echo "alias mvi='mv -i'"  >> /root/.bashrc
    
    echo "alias srl='systemctl restart squid'"  >> /root/.bashrc
    echo "alias sup='systemctl   start squid'"  >> /root/.bashrc
    echo "alias sdw='systemctl   stop  squid'"  >> /root/.bashrc
    echo "alias sus='systemctl  status squid'"  >> /root/.bashrc
    
    echo "alias swatch='cat /etc/squid/squid.conf'"  >> /root/.bashrc
    echo "alias setcvm='vim /etc/squid/squid.conf'"  >> /root/.bashrc
    echo "alias swatch='cat /etc/squid/squid.conf'"  >> /root/.bashrc

    echo "alias svlogs='tail -f /var/log/squid/access.log'"  >> /root/.bashrc
fi

echo '------------------------------------------------------------------------------end_bashrc_alias'
