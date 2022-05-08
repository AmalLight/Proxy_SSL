
ssh root@192.168.31.2 -t sh -c " apt install -y squid ;

    echo '------------------------------------------------------------------------------1'

    echo 'while IFS= read -r line ; do'             > /root/cat_without_comment.sh ;
    echo \"if [[ \\\${line:0:1} != '#' ]] ;\"      >> /root/cat_without_comment.sh ;
    echo 'then'                                    >> /root/cat_without_comment.sh ;
    echo \"if (( \\\${#line}     >  1  )) ;\"      >> /root/cat_without_comment.sh ;
    echo 'then'                                    >> /root/cat_without_comment.sh ;
    echo \"printf '%s\\n' \\\"\\\$line\\\"\"       >> /root/cat_without_comment.sh ;
    echo 'fi'                                      >> /root/cat_without_comment.sh ;
    echo 'fi'                                      >> /root/cat_without_comment.sh ;
    echo 'done < \$1'                              >> /root/cat_without_comment.sh ;

    ln -sf /root/cat_without_comment.sh /bin/cat_without_comment ;
    
    chmod 755 /root/cat_without_comment.sh
    
    echo '------------------------------------------------------------------------------2'
    
    cat_without_comment /etc/squid/squid.conf ;
    
    echo '------------------------------------------------------------------------------3'
"
