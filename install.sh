#!/bin/bash

INSTALLDIR="$HOME/.remhours"

mkdir $INSTALLDIR
mv * $INSTALLDIR
cd $INSTALLDIR
sudo apt install -y python3-virtualenv python3.10
virtualenv --python="/usr/bin/python3.10" env
$INSTALLDIR/env/bin/pip install -r requirements.txt
echo "Enter Cisin email:"
read UNAME
echo "Enter password:"
read -s PASSWD
echo -e "$UNAME\n$PASSWD" >> $INSTALLDIR/config
echo -e "alias remhours='$INSTALLDIR/env/bin/python main.py'" >> $HOME/.bashrc
$INSTALLDIR/env/bin/python main.py
echo "Installed successfully !"
echo -e "\nRUN 'remhours' command to get the results.\nYou can edit '$INSTALLDIR/config' file to edit your cisin user login credentials.\n"