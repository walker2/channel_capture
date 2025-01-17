
from ch_capture import simulate, plot_streaks, plot_first_and_last
from old_ch_capture import old_simulate
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle

def test_pmax():
    all_lengths = []
    conv_lengths = []
    len_diff = []
    
    pmaxes = np.arange(0.1, 0.25, 0.05)

    plt.figure()
    X = np.arange(0.04, 0.4, 0.04)
    pmin = 0.05
    exp_d = []
    for pmax in pmaxes:
        pmax = round(pmax, 2)
        print('PMAX IS {0:.2f}'.format(pmax))
        all_len, conv_len = simulate(N=20000, M=10, PMAX=pmax, PMIN=pmin)
        plot_streaks(PMAX=pmax)
        plot_first_and_last(PMAX=pmax)
        all_lengths.append(all_len)
        conv_lengths.append(conv_len)
        len_diff.append(all_len - conv_len)

        dirname = 'datapr_{0:.2f}'.format(round(pmax, 2) * 100)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        print(dirname)
        exp_d.append(pickle.load(open(dirname + '/delay.dump', 'rb')))

    print(exp_d)
    plt.plot(X, exp_d[0], label='pmax={}'.format(round(0.1, 2)))
    plt.plot(X, exp_d[1], label='pmax={}'.format(round(0.15, 2)))
    plt.plot(X, exp_d[2], label='pmax={}'.format(round(0.2, 2)))
    plt.xlabel('Lambda')
    plt.ylabel('Delay')
    plt.legend()
    plt.savefig('res/delay.png')
    plt.close()

    
    #print(all_lengths)
    #print(conv_lengths)
    #print(len_diff)
#
    #plt.figure()
    #plt.plot(pmaxes, all_lengths)
    #plt.xlabel('Probabilites')
    #plt.ylabel('Number of successes')
    #plt.savefig('res/alllen.png')
    #plt.close()
    #
    #plt.figure()
    #plt.plot(pmaxes, conv_lengths)
    #plt.xlabel('Probabilites')
    #plt.ylabel('Convoluted number of successes')
    #plt.savefig('res/convlen.png')
    #plt.close()
# #
    #plt.figure()
    #plt.plot(pmaxes, len_diff)
    #plt.xlabel('Probabilites')
    #plt.ylabel('Convoluted number of successes')
    #plt.savefig('res/lendiff.png')
    #plt.close()

def test_cheater():

    
    pmax = 0.2
    
    all_len, conv_len = simulate(N=50000, M=11, PMAX=pmax, PMIN=0.05, cheater=True)
    plot_streaks(PMAX=pmax, cheater=True)
    plot_first_and_last(PMAX=pmax, cheater=True)

    print(all_len)
    print(conv_len)
    print(all_len - conv_len)
    X = np.arange(0.04, 0.4, 0.04)
    dirname = 'datapr_{0:.2f}'.format(round(pmax, 2) * 100)

    plt.figure()    
    plt.plot(X, pickle.load(open(dirname + '/delay.dump', 'rb')), label='honest')
    plt.plot(X, pickle.load(open('cheater/delay.dump', 'rb')), label='cheating')
    plt.xlabel('Lambda')
    plt.ylabel('Delay')
    plt.legend()
    plt.savefig('res/cheater_delay.png')
    plt.close()

def old_test_cheater():
    pmax = 0.2
    all_len, conv_len = old_simulate(N=50000, M=10, PMAX=pmax, PMIN=0.05, cheater=True)
    plot_streaks(PMAX=pmax, cheater=True)
    plot_first_and_last(PMAX=pmax, cheater=True)

    print(all_len)
    print(conv_len)
    print(all_len - conv_len)



def main():
    # Should we watch all the lambdas? Yes, because strange things occur in higher lamdbas
    # So we would test lambdas from 0.04 to 0.6 with step 0.04
    # So, what should we do first? 
    #   1.    We should genereate sample that we found interesting in lab work
    #      Set number of users as 10, PMAX = 1, PMIN = 0.05 as usual, number of windows is 20k to make things faster
    #      User of every successfull window we should write to the list
    #      Then convolute list to accumulate series of successfull windows by one user
    #      Find maximum pair usernum-series of the list, find mean of series in list
    #      Plot some of the highest series as diagram. Should we print window number too? Maybe, this will be cool
    #      Then, take list of convoluted successfull windows and plot first 100 and last 100 entries to see if there any differences
    #      Calculate length of original "success" list and length of convoluted list, compare   
    #   
    #   2.   Repeate first step for number of different PMAXes, and make corresponding conclusions
    #       Plot length of different "success" lists. What about delay? Calculate number of messages sent by each user.
    #       Find configuration fast enough and honest to all users.
    #
    #
    #   3.  Create model of one cheating user and take best PMAX from step two for other users
    #       Test system like in first step. How one dishonest user would affect all system and others?
    #
    #  -- plot User_pr(Win_Num), should be easy enough. 10 graphs in one plot, one should rise up from another
    #test_pmax()
    #test_cheater()
    old_test_cheater()




main()