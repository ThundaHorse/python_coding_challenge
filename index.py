import csv
from pprint import pprint as pp

''' 
I decided to not use any associated libraries such as numpy or pandas in this scenario. I understand how to use the associated libraries but I wanted to challenge myself to keep my code modular and 'clean' and exhibit my understanding of python comprehension and code setup. 

My approach may be frowned upon by those who would rather use libraries such as pandas or numpy however I wanted to challlenge myself to solve this challenge and show that I had an understanding of how the tools worked without the 'crutches' of libraries. 

I opted to not use a class so that in case a specific function was to be extracted, it could be done so without instantiating a class and just take the function itself.
'''

output_data = {
    'dates': [],
    'spy': {
        'close_adj': [],
        'change': []
    },
    'input': {
        'close_adj': [],
        'change': []
    }
}


def parse_files(input, **kwargs):
    ''' Retrieve values from csv files, if a date range is specified, only select values from the range are retrieved from the files '''
    try:
        with open('spy.csv', newline='') as spycsv, open(input, newline='') as inputcsv:
            row1, row2 = csv.DictReader(spycsv), csv.DictReader(inputcsv)

            for r1, r2 in zip(row1, row2):
                output_data['dates'].append(r1['date'])
                output_data['spy']['close_adj'].append(float(r1['close_adj']))
                output_data['input']['close_adj'].append(
                    float(r2['close_adj']))

        ''' Checking optional parameters to see if date range is specified, if so, slice retrieved values so that they are within the given date range '''
        if 'date_range' in kwargs and len(kwargs['date_range']) == 2:
            starting = kwargs['date_range'][0]
            ending = kwargs['date_range'][1]

            starting_idx = 0
            ending_idx = 0

            with open('spy.csv', newline='') as csv_dates:
                date_counter = csv.DictReader(csv_dates)
                for i, obj in enumerate(date_counter):
                    if obj['date'] == starting:
                        starting_idx = i
                    if obj['date'] == ending:
                        ending_idx = i
            output_data['dates'] = output_data['dates'][starting_idx:ending_idx]
            output_data['spy']['close_adj'] = output_data['spy']['close_adj'][starting_idx:ending_idx]
            output_data['input']['close_adj'] = output_data['input']['close_adj'][starting_idx:ending_idx]
    except:
        if not '.csv' in input:
            raise
    return output_data


def rolling_mean(input, n):
    ''' Helper function to calculate a rolling mean '''
    cumsum, moving_avgs = [0], []
    for i, x in enumerate(input, 1):
        cumsum.append(cumsum[i - 1] + x)
        if i >= n:
            moving_avg = (cumsum[i] - cumsum[i - n]) / n
            moving_avgs.append(moving_avg)
    return moving_avgs


def percent_change(starting, current):
    ''' Calculates the daily percentage change for SPY and the input stock, (new - old) / old * 100'''
    return (float(current) - starting) / abs(starting) * 100


def calc_changes():
    ''' Use percent_change to calculate daily percentage changes '''
    for val1, val2 in zip(output_data['spy']['close_adj'], output_data['input']['close_adj']):
        output_data['spy']['change'].append(
            percent_change(output_data['spy']['close_adj'][0], val1))
        output_data['input']['change'].append(
            percent_change(output_data['input']['close_adj'][0], val2))


def calc_covariances():
    ''' Sum of the difference between daily percentage change minus the mean of the daily percentage changes times difference of daily percentage change minus mean of input stock divided by N '''
    output = []
    covars = []
    s_avg = sum(output_data['spy']['change']) / \
        len(output_data['spy']['change'])
    i_avg = sum(output_data['input']['change']) / \
        len(output_data['input']['change'])

    for val1, val2 in zip(output_data['spy']['change'], output_data['input']['change']):
        output.append((val1 - s_avg) - (val2 - i_avg))
        covars.append(sum(output) / len(output_data['dates']))

    return covars


def calc_variance():
    ''' Denominator for beta function, sum of the difference between dialy percentage change squared divided by N'''
    output = []
    var = []
    s_avg = sum(output_data['spy']['change']) / \
        len(output_data['spy']['change'])
    for val1 in output_data['spy']['change']:
        output.append((val1 - s_avg) ** 2)
        var.append(sum(output) / len(output_data['dates']))
    return var


def rolling(n, limit):
    ''' Generates quantities on a time series by taking only the most recent N data points. Drops each old element to add a new one. '''
    count = 0
    idx = 0
    arr = []
    temp = []

    while idx < len(n):
        temp.append(n[idx])
        count += 1
        if count % limit == 0:
            arr.append(temp)
            temp = []
            idx -= (limit - 1)
        idx += 1
    return arr


def beta_summer(arr):
    ''' Helper function to calculate the rolling sums using the rolling function, sums each sub list '''
    return [sum(x) for x in arr]


def calc_beta(covs, varis, **limiter):
    ''' Covariance of daily percent changes of S and M divided by variance of S (or covariance of S and S) and return an object that has daily, weekly, n-day, and monthly betas '''
    daily_betas = [x / y for x, y in zip(covs, varis)]
    beta_object = {
        'daily': [x / y for x, y in zip(covs, varis)],
        'n-day': [],
        'weekly': [],
        'monthly': []
    }

    if len(daily_betas) >= 7:
        beta_object['weekly'] = beta_summer(rolling(daily_betas, 7))
    if limiter and len(daily_betas) >= limiter['limiter']:
        beta_object['n-day'] = beta_summer(
            rolling(daily_betas, limiter['limiter']))
    if len(daily_betas) >= 30:
        beta_object['monthly'] = beta_summer(rolling(daily_betas, 30))

    return beta_object


if __name__ == '__main__':
    # Test using whole data population
    # parse_files('msft.csv')

    # Test using a limited date range instead of all
    parse_files('msft.csv', date_range=['1/29/1993', '2/12/1993'])

    # Call calc_changes() to calculate daily change
    calc_changes()
    # Call calc_covariances() to calculate covariances and store it in covars variable
    covars = calc_covariances()
    # Call calc_variance() to calculate variance and store it in varis variable
    varis = calc_variance()

    # Calculating beta object with and without a limiter (N day)
    # betas = calc_beta(covars, varis, limiter=5)
    betas = calc_beta(covars, varis)

    # Printing the beta object returned
    pp(betas)
