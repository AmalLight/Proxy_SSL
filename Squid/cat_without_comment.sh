while IFS= read -r line ; do
if [[ ${line:0:1} != '#' ]] ;
then
if (( ${#line}     >  1  )) ;
then
printf '%s\n' "$line"
fi
fi
done < $1
