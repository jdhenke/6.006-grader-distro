6.006 PSET to Grade Distributor
===============================

## Instructions

1. download the submissions
2. generate `students.txt` with `ls path/to/submissions | sed s#.pdf## > students.txt`
3. use `graders.txt`, which is ignored for safety here, but ping Joe for it if you need it
4.  update settings in `driver.py`
5. `python driver.py > assignments.json`

Details of the assignment can be found in `assignments.json`.

This will create csv files for each grader, named as `<grader_username>.csv` with the following columns.

* problem
* student
* grade
* comment

As it stands, the workflow is to upload each of them to google drive, open them as a spreadsheet (this will create a copy, as CSVs are not editable; use the new copy which is a regular spreadsheet) and individually share them with the graders.
