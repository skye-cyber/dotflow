from dotflow.tests.test_core import TestDotInterpreter

core_tester = TestDotInterpreter()
core_tester.test_basic_creation()
core_tester.test_connection()
core_tester.test_invalid_node_id()
core_tester.test_node_creation()
core_tester.test_node_not_found()
