# Clock IO

## Minimum Requirement

- Python 3.6
- Postgres 9.0+

## Installation

- `cd` into project folder
- Create a virtual environment
- Activate it and install the requirements `pip install -r requirements.txt`
- Create database
- Run migration `python manage.py migrate`
- Run the constraint installation script `psql -U postgres -d clock_io_db -f scripts/add_constraint.sql
`
- Run the code `python manage.py runserver`
