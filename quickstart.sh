#!/bin/sh

echo "GCP Cloud Build started at $(date)."

airflow db init

airflow dags list-import-errors --subdir ./dags/ >> import_errors.txt

if [ -f import_errors.txt ] then
    if [ -s import_errors.txt ] then
        echo "Error! DAGs have syntax errors. Please validate"
        echo import_errors.txt
        #exit 1
    else
        echo "No syntax errors found."
    fi
fi

echo "Validation ended at $(date)."