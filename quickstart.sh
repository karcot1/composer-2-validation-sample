#!/bin/sh

echo "GCP Cloud Build started at $(date)."

airflow db init

airflow dags list-import-errors --subdir ./dags/ >> import_errors.txt

if grep -q "No data found" import_errors.txt
then
    echo "No syntax errors found."
else
    echo "Error! DAGs have syntax errors. Please validate"
    cat import_errors.txt
    exit 1
fi

echo "Validation ended at $(date)."