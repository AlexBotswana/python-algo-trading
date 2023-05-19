import csv
import itertools
import time

def bruteforce(max_invest, data):
    i = 0
    nb_stocks = len(data)
    # var and list initialisation best solution (for best performance)
    lst_best_invest = []
    best_performance = 0
    best_invest = 0
    while (i<nb_stocks):
        i=i+1
        # find all combination (from 1 stock to nb_stocks)
        comb = itertools.combinations(data,i)
        # performance and invest calculation for a specific combination
        # print(i)
        for lst_stocks in comb:
            # var and list initialisation current solution
            lst_current_invest = []
            current_performance = 0
            current_invest = 0
            for stock in lst_stocks:
                if (max_invest >= current_invest + float(stock[1])):
                    current_invest = current_invest + float(stock[1])
                    current_performance = current_performance + float(stock[1])*float(stock[2])
                    lst_current_invest = lst_current_invest + stock
            #compare with the previous result to choose the best performance between 2 combinations
            if (best_performance < current_performance):
                best_performance = round(current_performance, 2)
                best_invest = current_invest
                lst_best_invest = lst_current_invest
        # print(lst_current_invest, current_invest, current_performance)
    print(f'\nInvest amount: {best_invest}€\nperformance: {best_performance}€\nStocks list: {lst_best_invest}\n')

lst_stocks = []

# Open the CSV file and insert data into the table
with open('db/data_stocks2.csv') as csvfile:
# with open('db/dataset1_training.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=";")
    #to remove first line (file's header)
    next(csvreader)
    for row in csvreader:
        lst_stocks.append(row)
    
begin = time.time()
bruteforce(500, lst_stocks)
end = time.time()

time_exec = end - begin
print("Execution time: ", time_exec, "seconds")