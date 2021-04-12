#! /bin/sh
## Colors for Text in shell
RED='\033[0;31m'
GREEN='\033[0;32m'
L_CYAN='\033[1;36m'
NC='\033[0m' # No Color

error_exit()
{
    echo -e "${RED}ERROR: $1 ${NC}"
    exit 1
}

## Create migration files and migrate the database
echo -e "${L_CYAN}Creating migration files and running database migrations...${NC}"
python manage.py makemigrations || error_exit "Error with makemigrations"
python manage.py migrate || error_exit "Error with migrate"
echo -e "${GREEN}[Success] Django Migrations Done!${NC}"
echo ""

## Initialize database with data_0331.json
echo -e "${L_CYAN}Initializing database with data from JSON file${NC}"
python manage.py loaddata data_0331.json || error_exit "Error with loaddata"
echo -e "${GREEN}[Success] Database initialized with data_0031.json!${NC}"
echo ""

## Add data from CSV files into database
echo -e "${L_CYAN}Importing data from CSV files${NC}"
python import_csv_data.py || error_exit "Error with import_csv_data"
echo -e "${GREEN}[Success] Static data from CSV files imported!${NC}"
echo""

## Add preference options to the database
echo -e "${L_CYAN}Adding preference options to database${NC}"
python add_preferences.py || error_exit "Error with add_preferencese"
echo -e "${GREEN}[Success] Preference options added to database!${NC}"

## Update covid compliance status
echo -e "${L_CYAN}Updating covid compliance status for each restaurant${NC}"
python update_compliant_status.py || error_exit "Error with update_comlpiant_status"
echo -e "${GREEN}[Success] Covid compliance status updated for each restaurant!${NC}"
