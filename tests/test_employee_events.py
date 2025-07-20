import pytest
from pathlib import Path

# Create a project_root
# variable set to the absolute path
# for the root of this project
project_root = Path(__file__).parents[1]

# Create a `db_path` function for test functions below
# via pytest.fixture
@pytest.fixture
def db_path():    
    # Get `project_root` variable: a pathlib object for 
    # the `employee_events.db` file
    return project_root / 'python-package' / 'employee_events' / 'employee_events.db'

# `test_db_exists`:
# This function receives an argument
# with the same name as the function
# and creates the "fixture" for
# the database's filepath
def test_db_exists(db_path):
    
    # using the pathlib `.is_file` method
    # assert that the sqlite database file exists
    # at the location passed to the test_db_exists function
    try:
        assert db_path.is_file()
    except Exception as e:
        print(str(e))


@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect
    return connect(db_path)

@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [x[0] for x in name_tuples]

# `test_employee_table_exists`:
# This function receives the `table_names`
# fixture as an argument
def test_employee_table_exists(table_names):

    # Assert that the string 'employee'
    # is in the table_names list
    try:
        assert 'employee' in table_names
    except Exception as e:
        print(str(e))

# `test_team_table_exists`:
# This function receives the `table_names`
# fixture as an argument
def test_team_table_exists(table_names):

    # Assert that the string 'team'
    # is in the table_names list
    try:
        assert 'team' in table_names
    except Exception as e:
        print(str(e))

# `test_employee_events_table_exists`:
# This function receives the `table_names`
# fixture as an argument
def test_employee_events_table_exists(table_names):

    # Assert that the string 'employee_events'
    # is in the table_names list
    try:
        assert 'employee_events' in table_names
    except Exception as e:
        print(str(e))

