# composer-2-validation-sample
Starter code for automated validation of Airflow DAGs

## About this project

**Overview**

This code is intended to serve as a starting point for automating DAG validation steps within a CI/CD pipeline. The project contains the following items:

1. A folder of sample dags (dags/)
2. A requirements.txt file that contains relevant packages needed for the python files in this repository
3. A validation file that executes a series of unit and integration tests (dag_validation.py)
4. A Dockerfile that installs the relevant packages from requirements.txt and executes the validation file
5. A yaml file (cb_airflow.yaml) that organizes the validation process and deploys with Cloud Build.

When this repository is run through a CI/CD pipeline, the following steps will occur in sequence (following the structure of cb_airflow.yaml):

1. A docker image will be built following the steps in the Dockerfile.
2. A docker container will be created and run using the previously built image. In this step, dag_validation.py will execute and output results. If all tests pass, the build continues to the next step. If any builds fail, the build as a whole also fails.
3. If all tests pass, the DAGs being tests are copied to the DAGs folder in the relevant composer environment.

To use this code as-is, please follow the steps below:
1. Fork this repository in GitHub
2. Connect your GitHub repository to GCP in the Cloud Build UI

<img width="1042" alt="image" src="https://github.com/karcot1/composer-2-validation-sample/assets/111666655/6d5473f0-6324-4bc1-a8e7-a3cf669bf170">

4. Create a Cloud Build Trigger in the GCP project that contains your composer environment. For "Configuration", select "Cloud Build configuraiton file (yaml or json)" and specify the location as "Repository". In the drop down box, select "cb_airflow.yaml"

<img width="559" alt="image" src="https://github.com/karcot1/composer-2-validation-sample/assets/111666655/45dd0e4c-42c5-4be5-a622-efd2225b66df">

5. In "Substitution variables", set "_COMPOSER_BUCKET" to the GCS location of your Compoer 2 environment's Cloud Storage bucket.

<img width="546" alt="image" src="https://github.com/karcot1/composer-2-validation-sample/assets/111666655/b7583e12-c1ac-4ca8-aaf7-1cbb96b4cb0e">

Once the trigger is created, run a manual execution to ensure all steps are working as expected.

To incorporate this code into your own project, either of the two options are feasible:
1. Fork this repository and substitue the example DAGs for your actual DAGs
2. Copy the dag_validation.py and Dockerfile into your own repsitory that contains your DAGs, and either follow the above steps to create a Cloud Build trigger, or integrate these steps into your existing CI/CD pipeline. 
