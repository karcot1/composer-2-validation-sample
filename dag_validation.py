import os
import logging
import unittest
import ast
from airflow.models import DagBag
from airflow import models
from airflow.utils.dag_cycle_tester import check_cycle
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s %(message)s')

def has_top_level_code(file_path):
    with open(file_path, 'r') as file:
        try:
            parsed_code = ast.parse(file.read())
            for node in parsed_code.body:
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
                    print("File {} contains top-level code".format(file_path))
                    return False
                print("No top-level code detected")
                return True
        except SyntaxError:
            #Syntax error in the file, it doesn't have top-level code
            print("Syntax Error")
            return True

class TestDagIntegrity(unittest.TestCase):
    LOAD_SECOND_THRESHOLD = 2
    def setUp(self):
        DAGS_DIR = os.getenv('INPUT_DAGPATHS', default='dags/')
        logger.info("DAGs dir : {}".format(DAGS_DIR))
        self.dagbag = DagBag(dag_folder = DAGS_DIR, include_examples = False)
        
    def test_import_dags(self):
        self.assertFalse(
            len(self.dagbag.import_errors),
            'DAG contains import failures. Errors: {}'.format(
                self.dagbag.import_errors
            )
        )

    def test_dag_loads_within_threshold(self):
        duration = sum((o.duration for o in self.dagbag.dagbag_stats), timedelta()).total_seconds()
        self.assertTrue(
            duration <= self.LOAD_SECOND_THRESHOLD,
            'DAG load times are above the given threshold'
        )
    
    def test_dag_task_cycle(self):
      no_dag_found = True
      for dag in self.dagbag.dags:
        no_dag_found = False
        check_cycle(self.dagbag.dags[dag])  # Throws if a task cycle is found.

      if no_dag_found:
          raise AssertionError("module does not contain a valid DAG")
    
    def test_dag_toplevelcode(self):
        assert True
        folder_path = 'dags/'
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                print(file_path)
                if file_path.endswith('.py'):
                    self.assertTrue(has_top_level_code(file_path))

    
    # def test_operator_parser(operator)
    #     assert True
    #     #TODO: not a test, but need a module that takes in an operator and identifies GCP resources needed for given operator

    # def test_service_account_persmission_check(self):
    #     assert True
    #     #TODO: nice to have - verify service account permissions

if __name__ == '__main__':
    unittest.main()