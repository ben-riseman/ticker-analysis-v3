# ticker-analysis-v3

## Purpose

ticker-analysis-v3 is built to parse and aid in the analysis of U.S. Politician's Financial Disclosures, which are publicly available here:
Senate Financial Disclosures & PTRs (two files): https://efdsearch.senate.gov/search/home/
House Financial Discloures & PTRs (one file): https://disclosures-clerk.house.gov/PublicDisclosure/FinancialDisclosure

The overall module is a collection of 2 scripts - da_pandas.py, and ptra_pandas.py. Each is constructed to allow for the search of, and later segmentation of larger Pandas DataFrames from imported Excel/CSV files. da_pandas is for Financial Disclosure Analysis, and ptra_pandas is for Periodic Transaction Report Analysis respectively.

This module is meant to be used as an accessory to politician-stock-getter module (still WIP). Both scripts parse two larger Excel/CSV files each (House or Senate) that are given in the same directory. 

( IMPORTANT: As of right now, the politican-stock-getter module is not finished, so the format of Excel/CSV files will be detailed below. The files are also currently hardcoded within the scripts for testing purposes. )

## How to Use
