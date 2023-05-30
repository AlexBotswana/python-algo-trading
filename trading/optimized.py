from tqdm import tqdm
import csv
import time
import sys

start_time = time.time()
# Check for custom cash investment (default = 500)
try:
    MAX_INVEST = float(sys.argv[2])
except IndexError:
    MAX_INVEST = 500


def main():
    # Check for filename input
    try:
        filename = "db/" + sys.argv[1] + ".csv"
    except IndexError:
        print("\nNo filename found. Please try again.\n")
        time.sleep(1)
        sys.exit()
    stocks_list = read_csv(filename)
    print(f"\nProcessing '{sys.argv[1]}' ({len(stocks_list)} valid stocks) for {MAX_INVEST}€ :")
    display_results(knapsack(stocks_list))

def read_csv(filename):
    # Import stocks data from csv file
    # Filter out corrupted data
    try:
        with open(filename) as csvfile:
            stocks_file = csv.reader(csvfile, delimiter=';')
            next(csvfile)       # skip first row
            stocks_list = []
            for row in stocks_file:
                if float(row[1]) <= 0 or float(row[2]) <= 0:
                    pass
                else:
                    stock = (
                        row[0],
                        int(float(row[1])*100),
                        float(float(row[1]) * float(row[2])/100)
                    )
                    stocks_list.append(stock)
            return stocks_list
    except FileNotFoundError:
        print(f"\nFile '{filename}' does not exist. Please try again.\n")
        time.sleep(1)
        sys.exit()

def knapsack(stocks_list):
    # Initialize the matrix (ks) for 0-1 knapsack problem
    # Get best stocks combination
    max_inv = int(MAX_INVEST * 100)     
    stocks_total = len(stocks_list)
    cost = []       
    profit = []     
    for stock in stocks_list:
        cost.append(stock[1])
        profit.append(stock[2])
    # Find optimal profit
    ks = [[0 for x in range(max_inv + 1)] for x in range(stocks_total + 1)]
    for i in tqdm(range(1, stocks_total + 1)):
        for w in range(1, max_inv + 1):
            if cost[i-1] <= w:
                ks[i][w] = max(profit[i-1] + ks[i-1][w-cost[i-1]], ks[i-1][w])
            else:
                ks[i][w] = ks[i-1][w]
    # Retrieve combination of stocks from optimal profit
    best_combo = []
    while max_inv >= 0 and stocks_total >= 0:
        if ks[stocks_total][max_inv] == \
                ks[stocks_total-1][max_inv - cost[stocks_total-1]] + profit[stocks_total-1]:
            best_combo.append(stocks_list[stocks_total-1])
            max_inv -= cost[stocks_total-1]
        stocks_total -= 1
    return best_combo

def display_results(best_combo):
    # Display best combination results
    print(f"\nMost profitable investment ({len(best_combo)} stocks) :\n")
    cost = []
    profit = []
    for item in best_combo:
        print(f"{item[0]} | {item[1] / 100} € | +{item[2]} €")
        cost.append(item[1] / 100)
        profit.append(item[2])
    print("\nTotal cost : ", sum(cost), "€")
    print("Profit after 2 years : +", sum(profit), "€")
    print("\nTime elapsed : ", time.time() - start_time, "seconds\n")

if __name__ == "__main__":
    main()
