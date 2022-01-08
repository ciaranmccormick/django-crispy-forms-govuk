migrate:
        mkdir -p data/db
        python sandbox/manage.py migrate

run:
        python sandbox/manage.py runserver localhost:8002

flake:
        flake8 --show-source crispy_forms_govuk

tests:
        pytest -vv --exitfirst tests/

quality: tests flake
