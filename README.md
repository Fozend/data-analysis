# data-analysis
Labs on Data Analysis

## Requirements
To install all necessary libraries, run the following command:

```bash
pip install -r requirements.txt
```

Lab 2 
Contains a jupyter notebook that works with VHI in different regions of Ukraine in the period from 1982 to 2024

Description:
Displays the VHI for a selected region in a given year
Shows extrema, mean, and median values from the table for the selected region and year
Analyzes the VHI for the selected range of years and regions
Identifies years with the highest number of droughts that affected more than a certain percentage of regions

To run it, open the lab2.ipynb file in Jupyter Notebook and run the cells

Lab 3

This lab contains a Python script that creates an interactive web app using Streamlit to analyze data from Lab 2.

Features:
Time series selection: Choose from VCI, TCI, or VHI.
Region selection: Choose a region for analysis.
Week & Year selection: Use sliders to filter by week and year.
Reset filters: Button to restore default settings.
Tabs: Display a table, filtered graph, and region comparison graph.
Graphs:
    Time series for the selected week and year range.
    Comparison of VCI, TCI, or VHI values for the selected region and others.
Sorting: Checkboxes to sort data ascending/descending (with warning if both are selected).
Layout: Interactive elements in one column, data in another.

To run it, , run the following command:

```bash
streamlit run lab3/lab3.py
```

vers1 - initial project with labs 2 and 3

vers1.1 - revised project with labs 2 and 3

Change log:
fixed and improved filter reset in lab 3
improved graph 3 in lab3
minor fixes and improvements in the lab3.py code
