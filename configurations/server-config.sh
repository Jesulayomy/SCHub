#!/usr/bin/env bash

# Upgrade and update
apt-get -y update
apt-get -y upgrade
# adds my most used aliases and customized prompt to the bashrc file
echo -e "# added by configure_aliases script from github.com/jesulayomy/configs/" | tee -a ~/.bashrc > ~/configure_aliases_output
echo -e "# C-compilation options\nalias gcce='gcc -Wall -Werror -Wextra -pedantic -std=gnu89'\n" | tee -a ~/.bashrc > ~/configure_aliases_output
echo -e "# Permissions Modifier\nalias x='chmod +x'\n" | tee -a ~/.bashrc > ~/configuration_output
echo -e "# Colorised prompt for PS1 and PS2\nPS1=\"\\[\\e[0;32m\\]/\\W \\[\\e[0;35m\\]\\$ \\[\\033[0m\\]\"\nPS2=\"\\e[0;36m\\]-> \\[\\033[0m\\]\"" | tee -a ~/.bashrc > ~/configuration_output
# adds the vimrc needed config for formatting text

echo -e "\" added by configure_vim script from github.com/jesulayomy/configs/\n" | tee -a ~/.vimrc > ~/configuration_output
echo -e "filetype indent on\nfiletype plugin on\nset number\nsyntax enable\nset cindent\nset autoindent\nhighlight ColorColumn ctermbg=gray\nset colorcolumn=80" | tee -a ~/.vimrc > ~/configuration_output

# Python3.10 installation
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip install --upgrade pip
apt install -y libssl-dev libffi-dev python3-dev
apt-get -y install pycodestyle
rm get-pip.py

# Install unzip and make utility
apt-get -y install apt-utils
apt-get -y install unzip
apt-get -y install build-essential
apt-get -y install make
apt-get -y install cmake

# Install requirements
apt-get install -y python3-lxml
pip3 install pep8==1.7.1
pip3 install email_validator==2.0.0.post2
pip3 install SQLAlchemy==2.0.9
pip3 install python-dotenv
pip3 install mysql-connector-python
pip3 install Flask==2.3.2
pip3 install Flask_Login==0.6.2
pip3 install Flask_Cors==3.0.10
pip3 install flasgger==0.9.7.1
pip3 install pandas==2.0.2
pip3 install gunicorn==20.1.0
pip3 install PyJWT
pip3 install openpyxl

cd /
# Download and install stderred
wget https://github.com/sickill/stderred/archive/refs/heads/master.zip
unzip master.zip
rm master.zip
cd stderred-master/
make
export LD_PRELOAD="/stderred-master/build/libstderred.so"
echo -e "export LD_PRELOAD=\"/stderred-master/build/libstderred.so\"" | tee -a ~/.bashrc
cd /

# Check Versions
clear

# Configures a server to work with nginx

apt-get -y update
apt-get -y upgrade
apt-get -y install nginx

# Disables Password authentication for ease of login
echo -e "    PasswordAuthentication no" | tee -a /etc/ssh/ssh_config

# Adds the custom X-Served-By Header to the default file
service nginx restart

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.33.0/install.sh | bash
export NVM_DIR="/root/.nvm"
nvm install v18.16.1
