import pytest
import slash
from slash.loader import Loader
import sys
import os
import slash.reporting
import slash.hooks

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_pytest():
    """
    Runs tests using pytest.
    """
    sys.exit(pytest.main(["tests/"]))

def run_slash():
    """
    Runs tests using slash.
    """

    @slash.hooks.register
    def report_test_summary():
        """
        Hook para imprimir un resumen de pruebas al final de la ejecución.
        """
        summary = slash.context.session.results.get_num_successful()
        failed = slash.context.session.results.get_num_failures()
        errors = slash.context.session.results.get_num_errors()

        print("\n===== RESUMEN DE PRUEBAS =====")
        print(f"✅ Pruebas exitosas: {summary}")
        print(f"❌ Pruebas fallidas: {failed}")
        print(f"⚠ Errores en ejecución: {errors}")
        print("=============================\n")

    with slash.Session() as session:
        with session.get_started_context():
            from conftest import driver
            session.fixture_store.push_scope('session')
            session.fixture_store.add_fixtures_from_dict({"driver": driver})

            # Cargar pruebas desde la carpeta "tests/"
            loader = Loader()
            tests = loader.get_runnables(["tests/"])
            if tests:
                result = slash.runner.run_tests(tests)
                sys.exit(0 if result and result.success else 1)
            else:
                print("No se encontraron pruebas para ejecutar.")
                sys.exit(1)


if __name__ == "__main__":
    if "--slash" in sys.argv:
        run_slash()
    else:
        run_pytest()
