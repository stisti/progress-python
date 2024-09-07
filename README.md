# progress

This is a progress meter for unix (and windows) pipelines, implemented in Python.

I made progress originally in C to solve a need I had 25 years ago.
Since then I have used it as a kind of "kata" and implemented it in several languages.

## Build

```
python -m venv .venv
source .venv/bin/activate
python -m pip install build
python -m build
```

## Test

```
ruff check
pytest
1..1000000 | ForEach-Object { $_ } | python -m progress >nul
```

## Install

```
python -m pip install dist/progress-0.0.1-py3-none-any.whl
```

## Usage
```
producer | progress | consumer
```

