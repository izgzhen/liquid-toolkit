Liquid Toolkit
=====

Android/Java toolkit with Python API based on https://github.com/izgzhen/liquid.

## Dependencies

- Python 3
  + `poetry installl; poetry shell`
- Java > 8
- `git clone https://github.com/semantic-graph/semantic-graph.py semantic`
- `git clone https://github.com/izgzhen/android-platforms`

## Features

Import graph visualization (`<depth>` is the maximum package namespace depth, `<op>` can be `-` or `=`):

```
python3 import-graph.py path/to/some.apk path/to/output.dot <depth> <op><filter-list>

# e.g.
python3 import-graph.py path/to/some.apk path/to/output.dot 2 -com.google,com.facebook
python3 import-graph.py ~/tmp/pinball.apk ~/tmp/pinball.dot 2 '=com.bingo,com.unity,com.chartboost'
```

## About pre-compiled jar

The liquid jar in this source repo is compiled from the above project and
checked-in for easier use. You can compile Liquid locally using SBT and copy
the jar in the same directory here as well.

