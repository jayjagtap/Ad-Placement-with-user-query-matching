import numpy as np
import pandas as pd
import sys 
import random
import math
random.seed(0)


#Code for greedy Method
def findHighestBiddergreedy(bids, advBudgetDict):
    highestBidder = None
    highestBid = -1
    for x in bids:
        if advBudgetDict[x] >= bids[x]:
            if bids[x] > highestBid:
                highestBidder = x
                highestBid = bids[x]
                
    return highestBidder, highestBid
        
def greedy(queries, advBudgetDict, query_bids):
    revenue = 0.0
    for x in queries:
        bids = query_bids[x]
       # Flag to check if advertisers have money
        flag = True
        for y in bids:
            if bids[y] <= advBudgetDict[y]:
                flag = False
                break
               
        if flag == True:
            continue
        else:
            highestBidder, highestBid = findHighestBiddergreedy(bids, advBudgetDict)
    #Add highest bid to revenue
        if(highestBidder ==  None):
            continue
        revenue += highestBid
    #Subtract the bid from advertiser budgtet
        advBudgetDict[highestBidder] -= highestBid 
    return revenue


def psiBid(remBudget, origBudget):
    # Get the ratio of spent budget
    ratioRemBudget = (origBudget - remBudget)/origBudget
    # Apply formula
    psi = 1 - math.exp(ratioRemBudget - 1)
    return psi

def findHighestBidderMSSV(advBudgetDict, remBudget, bids):
    highestBidder = None
    highestBid = -1
    for x in bids:
        # Consider the advertiser only if it has enough budget for the bid
        if remBudget[x] >= bids[x]:
            if highestBidder is not None:
                psiHigh = highestBid * psiBid(remBudget[highestBidder],advBudgetDict[highestBidder])
            else:
                psiHigh = -1
            psiCur = bids[x] * psiBid(remBudget[x],advBudgetDict[x])

            if psiCur > psiHigh:
                highestBid = bids[x]
                highestBidder = x
            # If same bid, choose the advertiser with smaller id
            elif psiCur == psiHigh:
                if x < highestBidder:
                    highestBidder = x
    return highestBidder, highestBid
                    
def mssv(queries,advBudgetDict, remBudget, query_bids):
    revenue = 0.0
    for x in queries:
        bids = query_bids[x]
       # Flag to check if advertisers have money
        flag = True
        for y in bids:
            if bids[y] <= advBudgetDict[y]:
                flag = False
                break
               
        if flag == True:
            continue
        else:
            highestBidder, highestBid = findHighestBidderMSSV(advBudgetDict, remBudget, bids)
       # print(revenue)
        revenue += highestBid
        remBudget[highestBidder] -= highestBid
        
    return revenue

def highestBidderbalance(advBudgetDict, bids):
    highestBidder = list(bids.keys())[0]
    for x in bids:
        if advBudgetDict[x] >= bids[x]:
            if advBudgetDict[x] > advBudgetDict[highestBidder]:
                highestBidder = x
            # If same budget, choose the advertiser with smaller id
            elif advBudgetDict[x] == advBudgetDict[highestBidder]:
                if x < highestBidder:
                    highestBidder = x
    return highestBidder

def balance(queries, advBudgetDict, query_bids):
    revenue = 0.0
    for x in queries:
        bids = query_bids[x]
        # Flag to check if advertisers have money
        flag = True
        for y in bids:
            if bids[y] <= advBudgetDict[y]:
                flag = False
                break
               
        if flag == True:
            continue
        else:
            #Find advertiser with highest Budget
            highestBidder = highestBidderbalance(advBudgetDict, bids)
        revenue += bids[highestBidder]
        advBudgetDict[highestBidder] -= bids[highestBidder]
    return revenue
            
        
def main():
    df = pd.read_csv("bidder_dataset.csv")
    #Dictionary of total budget of each bidder
    advBudgetDict = {}

    #Dictionary of dictionary keyword and bidders for each keyword
    query_bids = {}

    for i in range(0, len(df)):
        row_no = df.iloc[i]
        advId = row_no[0]
        query = row_no[1]
        bid = row_no[2]
        budget = row_no[3]
        
        if not np.isnan(budget):
            advBudgetDict[advId] = budget
        
        if query not in query_bids:
            query_bids[query] = {}
            
        if advId not in query_bids[query]:
            query_bids[query][advId] = bid
             
    #print(query_bids)
    #print(advBudgetDict)
    #Sum of all the advertisers budget
    optimal_revenue = sum(advBudgetDict.values())
    #print(optimal_revenue)

    with open('queries.txt') as f:
        queries = f.readlines()
    queries = [x.strip() for x in queries]
    #print(len(queries))
    #print(queries)
    method = sys.argv[1]
    revenue_generated = 0

    if method == "greedy":
        revenue = greedy(queries, advBudgetDict.copy(), query_bids)
    elif method == "mssv":
        revenue = mssv(queries, advBudgetDict.copy(), advBudgetDict.copy(), query_bids)
    elif method == "balance":
        revenue = balance(queries, advBudgetDict.copy(), query_bids)
    else:
        print("Invalid argument")
        return

    revenue_generated += revenue
    print(revenue_generated/optimal_revenue)
    
if __name__ == "__main__":
	main()
