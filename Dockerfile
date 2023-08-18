# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM python:3.11

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy dag code to container image
COPY DAGs /usr/src/dags
WORKDIR /usr/src/dags
CMD ["apache-airflow", "db", "init"]
CMD ["apache-airflow", "dags", 'list']

# Execute test commands

# CMD ["airflow", "db", "init"]
# CMD ["airflow", "dags", "list-import-errors", "--subdir", "dags/"]