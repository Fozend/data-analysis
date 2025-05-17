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

### To run it, open the lab2.ipynb file in Jupyter Notebook and run the cells

### WARNING: don't forget to install requirements, run the following command:

```bash
pip install -r requirements.txt
```

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

### To run it, run the following command:

```bash
streamlit run lab3/lab3.py
```

vers1 - initial project with labs 2 and 3

vers1.1 - revised project with labs 2 and 3

Change log:
fixed and improved filter reset in lab 3
improved graph 3 in lab3
minor fixes and improvements in the lab3.py code

### WARNING: don't forget to reinstall requirements, run the following command:

```bash
pip install -r requirements.txt
```

Lab 4

Contains a jupyter notebook that we perform various data manipulation tasks using both numpy arrays and pandas dataframes

Tasks:
Data Cleaning:

Handle missing values (represented as ?).

Data Selection:

Filter records where power consumption exceeds 5 kW and voltage exceeds 235V.

Select records with current between 19-20A, where the washing machine and fridge consume more than the boiler and air conditioner.

Randomly select 500,000 records and compute average values for three consumption groups.

Select records with average power consumption > 6 kW after 18:00, filtered by specific appliances (washing machine, dryer, fridge, lighting).

Handling Missing Data:

Address missing values.

Normalization & Standardization:

Implement manual normalization and standardization functions (without using sklearn).

Visualizations & Statistical Analysis:

Build a histogram with 10 specified bins.

Create a scatter plot for two numeric attributes.

Compute Pearson and Spearman correlation coefficients.

Perform One Hot Encoding on a categorical attribute.

Visualize multi-dimensional data effectively.

### To run it, open the lab4.ipynb file in Jupyter Notebook and run the cells

### WARNING: don't forget to reinstall requirements, run the following command:

```bash
pip install -r requirements.txt
```

Lab 5

Contains three separate Python scripts that implement the creation of a harmonic signal with noise, filtering this signal, and building an interactive interface using modern visualization libraries

Task 1

Description:

Matplotlib are used to create the GUI

The function harmonic_with_noise generates a harmonic signal with added noise:

Amplitude, Frequency, and Phase parameters define the harmonic

Noise Mean and Noise Covariance are used to create Gaussian noise

show_noise flag controls whether the noise is displayed on the plot

The GUI contains:

Sliders for adjusting amplitude, frequency, phase, and noise parameters (mean and covariance)

A Checkbox to toggle the visibility of the noise

A Reset Button to restore default parameters

After adjusting the parameters, the plot is updated automatically

If the noise parameters are changed, only the noise part of the signal is updated. The harmonic part stays as it was

Details:

The harmonic function is generated using the formula: y = A * sin(2πft + phase), where A is amplitude, f is frequency, t is time, and phase is the phase shift

Noise is generated using np.random.normal, with the mean and covariance passed as parameters

The CheckButtons widget allows toggling the visibility of the noise on the plot

### To run it, run the following command:

```bash
python lab5/lab5_1.py
```

Task 2

Description:

The harmonic signal with noise is filtered using a Butterworth filter from the scipy.signal.butter and scipy.signal.filtfilt methods

Parameters for the filter (fs and cutoff frequency) can be adjusted using sliders

### To run it, run the following command:

```bash
python lab5/lab5_2.py
```

Task 3

Description:

This task implements the same functionality as Tasks 1 and 2 but using Bokeh, a modern web-based library for interactive plotting

Instead of filters from the scipy library, added two custom Python filters (using NumPy) is applied to smooth the signal

### To run it, run the following command:

```bash
bokeh serve --show lab5/lab5_3.py
```

### WARNING: don't forget to reinstall requirements, run the following command:

```bash
pip install -r requirements.txt
```
Lab 6

This lab consists of two tasks focusing on linear regression, working with noisy data, and implementing gradient descent from scratch

Task 1

Description:
Generate linear data:
y=kx+b
Add normally distributed noise using np.random.normal() to simulate measurement errors

Visualize:

Initial line (true model)

Noisy points

Regression line obtained with:

Least Squares Method

numpy.polyfit

Used Least Squares Method formulas:

k = (∑(Xi − X^)(Yi − Y^) ) / ∑(Xi − X^)^2
b = Y^ − β1X^

Task 2: Gradient Descent for Linear Regression

Manually minimize the MSE loss function to estimate line parameters using batch gradient descent

Steps:

1. Initialize b, k, set learning_rate and number of iterations.

2. Compute predictions: yi^ = bi + ki*xi 

3. Calculate partial derivatives
∂L/∂b = −2 * 1/n * ∑(yi − yi^)
∂L/∂k = −2 * 1/n * ∑xi(yi − yi^)

4. Update parameters
b i+1 = bi − learning_rate * (∂L/∂b)
k i+1 = ki − learning_rate * (∂L/∂k)

5. Repeat 2-4 steps predicted number of iterations

Track and plot error vs. iterations

Visualization:
Add the result of gradient descent as a separate line.

Plot MSE convergence graph (MSE calculated using formula: 1/n * ∑(yi − yi^)^2)

Display final parameters for:

True values

LSM

Polyfit

Gradient Descent

### To run it, open the lab6.ipynb file in Jupyter Notebook and run the cells

### WARNING: don't forget to reinstall requirements, run the following command:

```bash
pip install -r requirements.txt
```