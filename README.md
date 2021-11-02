# People and Acquisition Facts

## About

This application takes constituent data, email data, and subscription data to generate two files: a "people" file containing a subset of data on each constituent from the three source files, and an "acquisition facts" file that aggregates statistics on when people in the dataset were acquired.

## Setup

This application requires Python 3 and Pandas. Please see [instructions](https://pandas.pydata.org/docs/getting_started/install.html) for Pandas installation. The recommended installation method for Pandas is to install as part of the [Anaconda](https://docs.continuum.io/anaconda/) distribution, which also installs Python. Ensure python has been added to your PATH environment variable, or replace every call to `python` below with the full path to python, e.g. `C:\Users\alexa\anaconda3\python.exe`.

## Quick Start

To get started right away, open a command prompt in the directory containing `generate_people.py`, then run `python generate_people.py --help` for usage. For more detailed instructions, see below.

## Run

* This application is run via command prompt.
* To run from the directory which contains `generate_people.py`, run: `python generate_people.py`. 
    * To run from a directory other than the one which contains `generate_people.py`, provide the path to the application, e.g. `python path\to\generate_people.py`.
* When the application is run with no additional parameters, it will search for constituent data, email data, and subscription data in the current directory, as `cons.csv`, `cons_email.csv`, and `cons_email_chapter_subscription.csv` respectively.
    * To specify a different input source for constituent data, use the `-c` flag followed by a full filepath (including filename), e.g. `-c path\to\some_cons.csv`
    * To specify a different input source for email data, use the `-e` flag followed by a full filepath (including filename), e.g. `-c path\to\some_cons_email.csv`
    * To specify a different input source for subscription data, use the `-s` flag followed by a full filepath (including filename), e.g. `-c path\to\some_cons_email_chapter_subscription.csv`

* When the application is run with no additional parameters, it will generate output files `people.csv` and `acquisition_facts.csv` in the current directory.
    * To specify a different output destination for people data, use the `-p` flag followed by a full filepath (including filename), e.g. `-p path\to\some_people.csv`
    * To specify a different output destination for acquisition facts data, use the `-a` flag followed by a full filepath (including filename), e.g. `-a path\to\some_acquisition_facts.csv`
    * Any directories specified as part of the path to output data must exist already.
* If the output files exist already, they will be overwritten.

## Usage Examples

These are usage examples only. Absolute file paths will differ on your machine.

Run from a directory containing `generate_people.py` and the input files with their default names (`generate_people.py`, `cons.csv`, `cons_email.csv`, and `cons_email_chapter_subscription.csv`). Output to default files (`people.csv` and `acquisition_facts.csv` in the current directory):
```
python generate_people.py
```

Run from a directory containing input files with their default names but *not* `generate_people.py`. Output to default files.
```
python C:\workspace\people\generate_people.py
```

Run from a directory containing `generate_people.py` and the input files with their default names. Output to the default file location, but rename people data to `my_people.csv`.
```
python generate_people.py -p my_people.csv
```

Run from a directory containing `generate_people.py` and a sub-directory `input` containing `cons.csv`, `cons_email.csv`, and `cons_email_chapter_subscription.csv`. Output people data and acquisition facts data to a sub-directory `output`. (Note that the `output` directory must already exist.):
```
python generate_people.py -c input\cons.csv -e input\cons_email.csv -s input\cons_email_chapter_subscription.csv -p output\people.csv -a output\acquisition_facts.csv
```

## Project Assumptions

The following assumption were made to complete this exercise. Under normal circumstances, these points would be clarified with colleagues or with the client:
* Constituents must be captured in the people data even if they have no associated primary email address.
    * If this assumption is incorrect, the merge of the constituents data with the emails data should use how='inner' instead of how='left'.
* The people.csv schema should be exactly as described, without key values.
    * In a real implementation, it might be useful to preserve `cons_id` or `cons_email_id`, and possibly to generate a new key, `people_id`.
* The acquisition_facts file should be a .csv file with a header line.
    * The exercise did not specify the file format or whether it should have a header line.
* Any order for acquisition_facts is acceptable.
    * Current implementation sorts by descending number of acquisitions. It may be useful to sort chronologically by date.
* Expected structure of input data is known to the user of this tool.
    * If this assumption is incorrect, additional validation should be performed on the input files, and more details added to the readme.