#!/usr/bin/env bash

# remove the previous schub folder
cd /root/
rm -rf SCHub/

# Add a fresh pull of the website
git clone https://$GIT_TOKEN@github.com/micoliser/SCHub.git
# Copy environment variables and sql-setup
cp .env SCHub/

# Generate a new datadump and cleanup unnecessary csv files
cd SCHub/data/
python3 generate_dump.py
rm *.csv
echo -e "\n\nKill gunicorn and create new data\n\n"

## Regenerate the data
pkill gunicorn
echo -e "\n\nMySQL: Enter root password\n\n"
cat setup_dev_db.sql | mysql -u root -p

# New gunicorn session
echo "Create a new tmux session and rerun api"
cd /root/SCHub/
tmux kill-session -t gunicorn-session
sleep 5

tmux new-session -d -s gunicorn-session
tmux send -t gunicorn-session.0 'gunicorn --workers=3 --access-logfile access.log --error-logfile error.log --bind 0.0.0.0:5000 api.app:app' ENTER

sleep 5
cd data/
echo -e "\n\nMySQL: Enter root password\n\n"
cat dump.sql | mysql -u root -p

# Rebuild the app, change to production server
# Also move the build folder to the schub production directory
echo -e "\n\nRun npm build version\n\n"
cd /root/SCHub/schub/
npm install
npm run build

cd build/static/js/
sed -i 's|http\://localhost\:5000|https\://www.schub.me|g' main.*js
cd /root/SCHub/schub/
cp -R build/* /var/www/html/schub/
service nginx restart

# Redeploy app on webserver
# ssh root@web.schub.me 'rm -rf /var/www/html/schub/*'
# scp -r -i /root/.ssh/id_rsa /root/SCHub/schub/build/* root@web.schub.me:/var/www/html/schub/
# ssh root@web.schub.me 'service nginx restart'
