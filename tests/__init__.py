import os
import webbrowser
from coverage import coverage
from config import PathsConfig

PRINT_CONSOLE = False
PRINT_HTML = True
OPEN_HTML = False

if __name__ == '__main__':
    """
    Run tests with coverage analysis.
    """

    DO_COVERAGE = PRINT_CONSOLE or PRINT_HTML

    if DO_COVERAGE:
        cov = coverage(branch=True, omit=['flask/*', '../tests/*'])
        cov.start()

    from tests.test_db import DatabaseTests
    try:
        import unittest
        unittest.main()
    except:
        pass

    if DO_COVERAGE:
        cov.stop()
        cov.save()

        if PRINT_CONSOLE:
            print('\n\nCoverage Report:\n')
            cov.report()

        if PRINT_HTML:
            html_path = os.path.join(PathsConfig.BASE_DIR, 'tests', 'tmp', 'coverage', 'index.html').replace('\\', '/')
            print('HTML version: ' + html_path)
            cov.html_report(directory='tmp/coverage')
            if OPEN_HTML:
                webbrowser.open_new_tab(html_path)

        cov.erase()
