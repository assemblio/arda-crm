source ./venv/bin/activate

if [ "$#" -ne 3 ]
then
    echo "Invalid number of parameters."
else
    python create_user.py "--username $1 --password $2 --role $3"
fi