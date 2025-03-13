This Program is for lab 8

It will complete the following task:

Use a function called get_latest_data(dates, cpi)
    It will reference pull_date
    And load data into the database up to that date

This function will be run using a loop to simulate various uses

We will compare the different methods (append, trunc, and incremental)

[x] Load in data to create original database
[x] Create function get_latest_data(file,date)
    [x] parse month + year
    [x] reference correct column (didn't need regex)
[] Write a function for each method of dataloading
        Pulls up to a date parameter
        Doesn't duplicate data (does it correctly I guess)
    [] _append - use sql
    [] _trunc - use sql
    [] _inc - use python script
[] Make a notebook to run it a bunch of times and print results (loop?)
[] Submit