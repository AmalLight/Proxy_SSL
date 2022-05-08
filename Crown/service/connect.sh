
echo ''
echo 'CLEAR' ; bash /root/Samael/journal_clr.sh

# --------------------------------------------------------

echo ''
echo 'Http  host: 192.168.31.2 , port: 8080'
echo 'Https host: 192.168.31.2 , port: 8443'
echo ''
echo 'Logs  Link: http://logs.crown.proxy.ka/'
echo 'Main  Link: http://main.crown.proxy.ka/'
echo ''

# --------------------------------------------------------

  kill -15 $(pgrep python3)
# kill -9  $(pgrep python3)

chmod 775 *
echo *** | sudo -S cp *.service /etc/systemd/system/

els=`ls *.service`

sudo systemctl daemon-reload

for el in $els;
do
    sudo systemctl stop    $el
    sudo systemctl start   $el
    sudo systemctl enable  $el
    sudo systemctl restart $el
done

sudo systemctl daemon-reload

sudo ln -sf /root/Crown/journal_see.sh /usr/bin/see2
sudo ln -sf /root/stop.sh              /usr/bin/stop
sudo ln -sf /root/restart.sh           /usr/bin/restart
