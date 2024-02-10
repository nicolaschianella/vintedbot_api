###############################################################################
#
# File:      rsync_hugo.sh
# Author(s): Nico
# Scope:     Send the project in hugo's test folder
#
# Created:   12 January 2024
#
###############################################################################

branch=$(git rev-parse --abbrev-ref HEAD)

if [[ ! "$branch" =~ ^(dev|main)$ ]]; then
    rsync -e "ssh" --exclude=".idea/" --exclude='.git/' --exclude="__pycache__/" \
    --exclude="/venv" --exclude="*.csv" --exclude="*.log" --exclude=".gitignore" \
    -rav . guys@guysmachine:/home/guys/vintedbot_api/tests/hugo
else
    echo "Branch is dev or main. Skipping rsync command."
fi
