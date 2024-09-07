# progress

This is a progress meter for unix pipelines, implemented in Python.

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
1..1000000 | ForEach-Object { $_ } | python -m progress >nul
```

## Usage
```
producer | python3 progress.py | consumer
```

