#!/bin/sh

echo "GCP Cloud Build started at $(date)."

airflow db init

airflow dags list-import-errors --subdir ./dags/ >> import_errors.txt

if [ -s import_errors.txt ] 
then
    echo "Error! DAGs have syntax errors. Please validate"
    cat import_errors.txt
    #exit 1
else
    echo "No syntax errors found."
fi

echo "Validation ended at $(date)."