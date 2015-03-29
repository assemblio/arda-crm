source ./venv/bin/activate

if [ "$#" -ne 2 ]
then
    echo "Invalid number of parameters."
else
    python init.py --username $1 --password $2
fi