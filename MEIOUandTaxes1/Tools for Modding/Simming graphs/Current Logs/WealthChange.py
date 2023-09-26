from matplotlib import pyplot as plt
import pandas as pd

def get_data(t, i):
    lst = []
    loc = 0

    while True:
        loc = t.find(i, loc)

        if loc != -1:
            end = t.find('\n', loc)
            lst.append(float(t[loc:end].strip().split(':')[1].strip()))
            loc = end
        else:
            break

    return lst

if __name__ == '__main__':
    with open('game.log') as f:
        t = f.read()
        
        Innate = get_data(t, 'WealthChange Innate')
        Gold = get_data(t, 'WealthChange Gold')
        Property = get_data(t, 'WealthChange Property')
        Wages = get_data(t, 'WealthChange Wages')
        Infra = get_data(t, 'WealthChange Infra')
        Manpower = get_data(t, 'WealthChange Manpower')
        StateInc = get_data(t, 'WealthChange StateInc')
        ExtraTax = get_data(t, 'WealthChange ExtraTax')
        itr = range(1, len(Innate) + 1)

        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Gold, label="Gold")
        plt.plot(itr, Property, label="BU Property")
        plt.plot(itr, Wages, label="Wages")
        plt.plot(itr, Infra, label="Infra")
        plt.plot(itr, Manpower, label="Manpower")
        plt.plot(itr, StateInc, label="State Income")
        plt.plot(itr, ExtraTax, label="Special Taxes")

        plt.legend(loc=2, ncol=2)

        plt.show()