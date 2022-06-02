# Movies API
Finds producers with maximum and minimum interval between two prizes won.

# Dependencies
 - Python3.9 (May work Python3.6+)
 - Linux (Use vary in others platforms)
 - Curl (Http requests): `apt update && apt install curl`

# Installing Python Modules
 - Flask==2.1.2, pandas==1.4.2, pandasql==0.7.3, environs==9.5.0 and pytest==7.1.2:  
`pip3 install -r <project_dir>/requirements.txt`

# Running

### Default Movie List (`<project_dir>/default_movie_list.csv`)
 - `cd <project_dir>`
 - `export PYTHONPATH=$(pwd)`
 - `python3 src/app.py`

### Custom Movie List
 - `cd <project_dir>`
 - `export PYTHONPATH=$(pwd)`
 - `export MOVIES_CSV=<custom_movie_list.csv>`
 - `python3 src/app.py`

### HTTP Request
 - `curl --request GET 'http://127.0.0.1:5000/producers/winners/min_max_win_interval'`:
```json
{
  "max": [
    {
      "followingWin": 1990,
      "interval": 6,
      "previousWin": 1984,
      "producer": "Bo Derek"
    }
  ],
  "min": [
    {
      "followingWin": 1990,
      "interval": 6,
      "previousWin": 1984,
      "producer": "Bo Derek"
    }
  ]
}
```

# Running tests
 - `cd <project_dir>`
 - `python3 -m pytest -v tests`:

```
======================================= test session starts ========================================
platform linux -- Python 3.9.9, pytest-7.1.2, pluggy-1.0.0 -- /home/rodolfo/venvs/movies_api/bin/python3
cachedir: .pytest_cache
rootdir: /home/rodolfo/movies_api
collected 8 items                                                                                  

tests/integration_test.py::test_empty_response[default_none_won.csv] PASSED                  [ 12%]
tests/integration_test.py::test_empty_response[no_movies.csv] PASSED                         [ 25%]
tests/integration_test.py::test_empty_response[one_won.csv] PASSED                           [ 37%]
tests/integration_test.py::test_empty_response[two_same_producer_movies_one_won.csv] PASSED  [ 50%]
tests/integration_test.py::test_two_wins_same_year PASSED                                    [ 62%]
tests/integration_test.py::test_producers_same_win_interval_max_min PASSED                   [ 75%]
tests/integration_test.py::test_default_movies_csv PASSED                                    [ 87%]
tests/integration_test.py::test_default_all_won PASSED                                       [100%]

======================================== 8 passed in 0.82s =========================================
```