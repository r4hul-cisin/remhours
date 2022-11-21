#!/bin/bash

INSTALLDIR="$HOME/.remhours-test"
bold=$(tput bold)
normal=$(tput sgr0)

mkdir $INSTALLDIR
cp * $INSTALLDIR
cd $INSTALLDIR
sudo apt install -y python3-virtualenv python3.10
virtualenv --python="/usr/bin/python3" env
$INSTALLDIR/env/bin/pip install -r requirements.txt

if [ $? -eq 0 ]; then
  echo "Enter Cisin email:"
  read UNAME
  echo "Enter password:"
  read -s PASSWD
  echo -e "$UNAME\n$PASSWD" >> $INSTALLDIR/config
else
  echo "Requirements not satisfied."
  exit 1
fi

#echo -e "alias remhours='$INSTALLDIR/env/bin/python main.py'" >> $HOME/.bashrc
$INSTALLDIR/env/bin/python3 main.py
echo "${bold}Installed successfully !${normal}"
echo -e "\nRun ${bold}remhours${normal} command to get the results.\nYou can edit ${bold}$INSTALLDIR/config${normal} file to edit your cisin user login credentials.\n"