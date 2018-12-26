

from ch_capture import simulate, plot_streaks, plot_first_and_last
import numpy as np
import matplotlib.pyplot as plt

def test_pmax():
    all_lengths = []
    conv_lengths = []
    len_diff = []
    
    pmaxes = np.arange(0.20, 1, 0.15)
    for pmax in pmaxes:
        pmax = round(pmax, 2)
        print('PMAX IS {0:.2f}'.format(pmax))
        all_len, conv_len = simulate(N=20000, M=10, PMAX=pmax, PMIN=0.05)
        plot_streaks(PMAX=pmax)
        plot_first_and_last(PMAX=pmax)
        all_lengths.append(all_len)
        conv_lengths.append(conv_len)
        len_diff.append(all_len - conv_len)

    print(all_lengths)
    print(conv_lengths)
    print(len_diff)

    plt.figure()
    plt.plot(pmaxes, all_lengths)
    plt.xlabel('Probabilites')
    plt.ylabel('Number of successes')
    plt.savefig('res/alllen.png')
    plt.close()
    
    plt.figure()
    plt.plot(pmaxes, conv_lengths)
    plt.xlabel('Probabilites')
    plt.ylabel('Convoluted number of successes')
    plt.savefig('res/convlen.png')
    plt.close()

    plt.figure()
    plt.plot(pmaxes, len_diff)
    plt.xlabel('Probabilites')
    plt.ylabel('Convoluted number of successes')
    plt.savefig('res/lendiff.png')
    plt.close()

def test_cheater():
    

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
    test_pmax()




main()