#######################################

# NPM Package Checker
# Author: Hassan Khan Yusufzai
# GitHub: https://github.com/Splint3r7
# Twitter: https://twitter.com/Splint3r7

########################################

if [[ $1 == '-h' ]] || [[ $1 == '--help' ]]; then
	echo "[+] Useage:	./npm-checker.sh -p <package name>"
	echo "[+] Useage:	./npm-checker.sh -f <list of package names>"
	exit 1
fi

RED='\033[0;31m'
BWhite='\033[1;37m'
GREEN="\033[0;32m"
RESET="\033[0m"
NC='\033[0m'
YELLO="\033[0;33m"
Purple='\033[0;35m'
IRed='\033[0;91m' 
Cyan='\033[0;36m'


NPMCHECKER () {

exec=$(npm view ${package} maintainers.email 2>&1)

if [[ $exec =~ "npm ERR!" ]]; then
	echo -e "[${RED}-${NC}] ${YELLO}Not a Valid NPM package${NC}"
	exit
else

	echo -e "[${GREEN}+${NC}] ${YELLO}Checking NPM Package${NC}: $package"

	if [[ $exec =~ "maintainers"  ]]; then
		email=$(echo -e "$exec \n" | awk '{print $3}')
		emails=$(echo -e "$email \n" | cut -d "'" -f2 | cut -d "@" -f2 | sort -u | awk 'NF' > /tmp/tmp.txt)
		while read e_mails; do
			hosts=$(echo $e_mails)
			host_cmd=$(host $hosts)

			if [[ $host_cmd =~ 'not found: 2(SERVFAIL)' ]]; then
				echo -e "[\xE2\x9D\x8C] ${RED}Vulnerable Host${NC} -> [$hosts]"
			else
				echo -e "[${GREEN}\xE2\x9C\x94${NC}] Secure Host -> [$hosts]"
			fi
		done < /tmp/tmp.txt
		
	else
		mail=$(echo -e "$exec" | cut -d "'" -f2 | cut -d "@" -f2 | sort -u)
		host_cmd=$(host $mail)

		if [[ $host_cmd =~ 'not found: 2(SERVFAIL)' ]]; then
			echo -e "[\xE2\x9D\x8C] ${RED}Vulnerable Host${NC}-> [$mail]"
		else
			echo -e "[${GREEN}\xE2\x9C\x94${NC}] Secure Host -> [$mail]"
		fi
fi
fi
}

if [[ $1 == '--package' ]] || [[ $1 == '-p' ]]; then
	
	package=$2
	NPMCHECKER

fi

if [[ $1 == '--file' ]] || [[ $1 == '-f' ]]; then
	input_file=$2
	for package in $(cat $input_file); do
		NPMCHECKER
	done

fi
