import matplotlib.pyplot as plt
import numpy as np
import math

# distribution
# 10% losing 5x risk
# 30% losing 1x risk
# 55% winning 2x risk
# 5% winning 10x risk
'''
l = [-5, -5, -1, -1, -1, -1, -1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10]

balance = int(input("Starting Balance: "))
init_balance = balance
while True:
    try:
        price = np.random.uniform(1, 500)
        print("#" * 10, "Price of stock", "#" * 10)
        print("%.2f SEK / Share " % price)

        while True:
            rpt = float(input("Risk per trade: "))
            while True:
                numshares = int(input("Number of shares to buy: "))
                if price * numshares > balance:
                    print("Not enough funds...")
                else:
                    break
            print("#" * 10, "Your position", "#" * 10)
            print("%.2f SEK" % (numshares * price))
            risk = numshares * rpt
            print("Your risk: %.2f (of account: %.2f %%)" %
                  (risk, risk / balance * 100))

            pr = input("Proceed? (y/n)")
            if pr == "y":
                break

        # pick return uniformly from distribution
        p = int(np.random.uniform(1, 20))

        res = l[p] * risk

        print("#" * 10, "Result", "#" * 10)
        print("Outcome: ", res)

        balance = balance + res
        print("New balance: ", balance)

        if balance < 0.1 * init_balance:
            print("You lost the game!")
            break
        if balance > 1.5 * init_balance:
            print("Congratulations, you won the game!")
            break

    except KeyboardInterrupt:
        break
'''


## SIMULATION ###

def find_max(d):
    m = 0
    for val in d:
        if val[0] > m:
            m = val[0]
            xp = val[1]
    return m, xp

    # simulate above program over 1000 iterations
    # risking 1 % of account / trade
    # distributions of risk outcomes (win / loss)


# BIOTECH APPROVAL PROBABILITIES
# ADVANCED
# prob
#
#
#
#
#
#


# SIMPLIFIED
# from start to market: 0,09615693623 ... (100x if reach market)
w = 0.09615693623  # prob / success for each phase
sizeKelly = 100 / (100 * w - (1 - w))

drug_dev_years = 10
investing_lifetime_years = 80
iterations = int(investing_lifetime_years / drug_dev_years)
init_balance = 10000

final = []
size = [sizeKelly, sizeKelly * 2, sizeKelly * 3, sizeKelly * 4]
labels = ["Kelly", "Double Kelly", "Tripple Kelly", "Suicide"]
for i in range(len(size)):
    final.append([init_balance])

print("#" * 10, "START SIMULATION", "#" * 10)
# for years
for i in range(iterations):

    # for every stock
    for k, s in enumerate(size):
        temp = []
        num_stocks = math.floor(100 / (s))

        # prev balance
        bal = final[k][-1]
        # for ever position
        for j in range(num_stocks):
            price = np.random.uniform(1, 200)
            p = int(np.random.uniform(1, 100))

            # 99 outcomes = 0
            if p <= 92:
                x = -1
            # one is a 100 bagger
            else:
                x = 100
            # kelly
            shares = math.floor(s / 100 * bal / price)
            pos = shares * price
            res = pos * x

            temp.append(res)

        outcome = sum(temp)
        new_bal = bal + outcome
        if outcome < init_balance * 0.1:
            outcome = 0
        final[k].append(new_bal)

print("#" * 10, "RESULT", "#" * 10)
print("Initial investment: ", init_balance)
for i in range(len(labels)):
    print("%s end balance: %.2f" % (labels[i], final[i][-1]))

for i in range(len(final)):
    plt.plot(final[i], label=labels[i] + "= " +
             str(round(size[i], 2)) + " % of Account / position")
# plt.plot(final[0], label="kelly")
plt.title("Initial Investment of " + str(init_balance) + " SEK")
plt.xlabel("Iterations (Development cycle = 10years)")
plt.ylabel("Account Balance (SEK)")
plt.legend()
plt.yscale(u'log')
plt.show()
exit()


l = [-5, -5, -1, -1, -1, -1, -1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10]
# l_kel = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -
# 1, -1, -1, -1, -1, 10, 10, 10, 10, 30, 30]
# initial balance
balance = 1000
# iterations
iterations = 1000
# risk in % for each trade
risk_trade = [1, 5, 10, 15, 20, 30]
max_acc_expo = 1

# KELLY
# f(x) = 0.1log(1-5x)+0.3log(1-x)+0.55log(1+2x)+0.05log(1+10x)
foo = []
for xp in range(0, 100, 1):
    x = xp / 100
    f = 0.1 * math.log(1 - x) + 0.3 * math.log(1 - 0.1 * x) + \
        0.55 * math.log(1 + 0.2 * x) + 0.05 * math.log(1 + x)
    # f = 0.7 * math.log(1 - x) + 0.2 * math.log(1 + 10 * x) + \
    #    0.1 * math.log(1 + 30 * x)
    foo.append([f, x])

m, xval = find_max(foo)
print("Val: ", m, "Max betting size: ", xval)
d = [item[0] for item in foo]
xp = [item[1] for item in foo]

plt.plot(xp, d)
plt.axvline(x=xval, color='r', label="Max betting size")
plt.legend()
plt.show()
# END KELLY

##
# print settings
print("#" * 10, "Simulation with", "#" * 10)
print("Initial balance: ", balance)
print("Iterations: ", iterations)
print("Risk per trade: ", risk_trade)

# init outcome
out = []
kellyBet = []
temp = []
for i in range(len(risk_trade)):
    temp.append(balance)

# append initial balance
out.append(temp)
kellyBet.append(balance)

init_balance = balance

for i in range(iterations):
    temp = []

    # price and outcome should be same for all position sizes
    # price
    price = np.random.uniform(1, 500)
    # pick return uniformly from distribution
    p = int(np.random.uniform(1, 20))
    for j, val in enumerate(risk_trade):
        # risk per trade in currency
        rpt = val / 100 * price
        # num shares to buy
        numshares = math.floor(out[i][j] * max_acc_expo / price)
        # total risk
        risk = numshares * rpt

        # outcome
        res = l[p] * risk
        balance = out[i][j] + res

        if balance < init_balance * 0.1:
            balance = 0

        temp.append(balance)

    # append result for all R
    out.append(temp)

    # kelly
    rpt_kelly = xval * price
    numshares = math.floor(kellyBet[i] * max_acc_expo / price)
    risk = numshares * rpt_kelly
    res = l[p] * risk
    balance = kellyBet[i] + res
    if balance < init_balance * 0.1:
        balance = 0

    kellyBet.append(balance)

# filter out result
result = []
for i in range(len(risk_trade)):
    foo = [item[i] for item in out]
    result.append(foo)

# plot R trades
for i, val in enumerate(result):
    temp = 'R=' + str(risk_trade[i])
    plt.plot(val, label=temp)

# plot kelly
plt.plot(kellyBet, label="Kelly=" + str(xval * 100))

plt.xlabel("Number of trades")
plt.ylabel("Portfolio Value (SEK)")
plt.title("Portfolio Performance")
plt.yscale(u'log')
plt.legend()
plt.show()
