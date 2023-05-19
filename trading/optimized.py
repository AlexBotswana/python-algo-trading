import  csv
import  time

def optimized(max_invest, data):
    nb_stocks = len(data)
    best_invest = 0
    best_performance = 0
    lst_best_invest = []
    
    def combinations(lst_stocks, idx, invest, performance):
        nonlocal best_invest, best_performance, lst_best_invest
        
        if idx == nb_stocks:
            if performance > best_performance:
                best_invest = invest
                best_performance = round(performance, 2)
                lst_best_invest = lst_stocks
            return
        
        stock = data[idx]
        if invest + float(stock[1]) <= max_invest:
            combinations(lst_stocks + [stock], idx + 1, invest + float(stock[1]), performance + float(stock[1])*float(stock[2]))
        combinations(lst_stocks, idx + 1, invest, performance)
    
    combinations([], 0, 0, 0)
    
    print(f'\nInvest amount: {best_invest}€\nperformance: {best_performance}€\nStocks list: {lst_best_invest}\n')

lst_stocks = []

# Open the CSV file and insert data into the table
with open('db/dataset1.csv') as csvfile:
# with open('db/data_stocks2.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=";")
    #to remove first line (file's header)
    next(csvreader)
    for row in csvreader:
        lst_stocks.append(row)
    
begin = time.time()
optimized(500, lst_stocks)
end = time.time()

time_exec = end - begin
print("Execution time: ", time_exec, "seconds")