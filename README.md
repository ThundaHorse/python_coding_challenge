# Python Rolling Beta Coding Assignment

---

Provide code that computes the rolling beta (explained below) of MSFT with respect to SPY. Your code should fetch daily price data from the csv files provided in the attachments, and compute rolling beta between the two stocks, e.g. on any given day the beta should be computed over the trailing N-day period (rolling window). Please use python and associated libraries to complete the assignment.

**Rolling Beta Beta**: Beta is a measure of the correlation between two time series. In this case, the two time series are the SPY daily percentage change (call it **S**) and the MSFT daily percentage change (call it **M**).

**Beta of MSFT with respect to SPY** =

```python
COVARIANCE(S, M) / VARIANCE(S)
```

, where

```python
COVARIANCE(S,M) = SUM((S − MEAN(S)) ∗ (M − MEAN(M))) / N
```

, for

```python
N = N data points per time series
```

, and

```python
VARIANCE(S) = COVARIANCE(S,S)
```

**Rolling Quantity:** Rolling Quantity refers to the process of generating quantities on a time series by taking only the most recent **N** data points into account. As you progress in the time series, you drop each old element and add a new one. For example, given the sequence:

< 2,1,4,5,6,8 >

**Rolling of SUM(N=3)** would be:

```python
7 (2 + 1 + 4),10 (1 + 4 + 5),15 (4 + 5 + 6),19 (5 + 6 + 8)
```

## Things to think about

• When computing a rolling beta, there are more efficient ways of doing this than brute force, e.g. we can use intermediate computations from the previous day's calculation to make today's more efficient.
• Beta is an ordinary least squares statistic and so it is sensitive to outliers. You may want to have some way of handling these outliers. For example, you may want to cap any single day move to 5%.
• Your script should be flexible both on the "lookback" period (how much history you want to include for any point) as well as the aggregation period (daily, weekly, n-day, monthly betas).
• Extra points for making the solution modular and extensible, e.g. we might want to "plug in" our own clipping routine, or data source, or aggregation routine (e.g. code that takes daily inputs and samples it in different ways before feeding it to the estimator). To the extent that your code can be extensible with respect to these ideas, it will be preferable.
