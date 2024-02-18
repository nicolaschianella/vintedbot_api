###############################################################################
#
# File:      rsync_prod.sh
# Author(s): Nico
# Scope:     Send the project in the prod folder
#
# Created:   12 January 2024
#
###############################################################################

branch=$(git rev-parse --abbrev-ref HEAD)

if [[ "$branch" =~ (main)$ ]]; then
    rsync -e "ssh" --exclude=".idea/" --exclude='.git/' --exclude="__pycache__/" \
    --exclude="/venv" --exclude="*.csv" --exclude="*.log" --exclude=".gitignore"\
    -rav . guys@guysmachine:/home/guys/vintedbot_api/vintedbot_prod
else
    echo "Branch is not main. Skipping rsync command."
fi
