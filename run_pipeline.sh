#!/bin/sh
#run converter first, and then only run analysis if covnerter did nto fail
python converter.py && python data_analysis.py