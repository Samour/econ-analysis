# Economic analysis

Various scripts & datasets for analyzing economic info

## Setup

It's highly recommended to set up a virtual environment

```
python3 -m venv venv
```

Then to activate the virtual env

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## Run tests

```
python3 -m unittest discover
```

## Linting

Style linting:

```
# Report on style violations without changing the files
black --check analysis

# Auto-fix style violations
black analysis
```

Type linting:

```
mypy --strict analysis
```

## Running

Available entry points:

- `tax_rates_over_time`

Run the specific package

```
python3 -m analysis.<package>
```

Eg. to run `tax_rates_over_time`:

```
python3 -m analysis.tax_rates_over_time
```
