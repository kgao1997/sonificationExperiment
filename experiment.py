import winsound
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import random
random.seed(1337) #for consistency

def generate_data(target_r):
    data_x = np.linspace(0, 1, 100)
    data_y = []
    while len(data_y) < 100:
        new_data = np.random.normal(0, 1, 1)
        if new_data <= 2 or new_data >= -2:
            data_y.append(new_data[0])
            
    data_y = data_y / np.linalg.norm(data_y)

    r = np.corrcoef(data_x, data_y)
    r_z = r[0, 1]

    delta = ((r_z - 1) * (target_r * target_r + r_z) + math.sqrt(target_r * target_r * (r_z * r_z - 1) * (target_r * target_r - 1))) / ((r_z - 1) * (2 * target_r * target_r + r_z - 1))

    for (i, line) in enumerate(zip(data_x, data_y)):
        x_coor = line[0]
        old_y_coor = line[1]
        y_coor = (delta * x_coor + (1 - delta) * old_y_coor) / (math.sqrt(delta * delta + (1-delta) * (1 - delta)))
        data_y[i] = y_coor

    data_y = data_y / np.linalg.norm(data_y)

    old_y_coors_mean = np.mean(data_y)
    old_y_coors_std = np.std(data_y)
    data_y = ((data_y - old_y_coors_mean) * 0.2 / old_y_coors_std) + 0.5

    return (data_x, data_y)

def play_sound(data):
    converted_data = (data * 1000) + 1000
    for d in converted_data:
        winsound.Beep(int(d), 100)
        
#function by which the experiment is conducted. get user feedback with '1' or '2', and store test data (true r, direction, mod_r)
#function by which the experiment is conducted. get user feedback with '1' or '2', and store test data (true r, direction, mod_r)
def sonification_experiment():
    #approach = ['above', 'below']
    #true_rs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    #for testing/single trial use
    approach = ['above']
    true_rs = [0.5]
    max_judgements = 50 #starting value, can adjust if onerous
    n_judgements = 0
    #record experiment data into pandas dataframe
    exp_df = pd.DataFrame(columns = ['true_r', 'test_r', 'approach', 'correct'])
    df_cols = ['true_r', 'test_r', 'approach', 'correct']
    flip_arr = [True, False]
    #basic first: iterate along both approaches, and true r values
    for a in approach: 
        for r in true_rs: 
            if a == 'above': 
                test_r = r + 0.1 #set the test r value
                test_count = 0
                while test_count < 20: 
                    print('count num: ' + str(test_count))
                    test_count += 1
                    (xs, true_ds) = generate_data(r)
                    (xs, test_ds) = generate_data(test_r)
                    flip_flag = random.randint(0,1)
                    if flip_flag == 0:
                        play_sound(true_ds)
                        time.sleep(2) #delineate the two beeps
                        winsound.Beep(440, 1000) #beep in middle to show deliniation
                        time.sleep(2)
                        play_sound(test_ds)
                        judgement = -1
                        while (judgement in [1, 2]) == False: #force the user to give a good input
                            judgement = input("which audio had higher correlation? Input '1' if the first, '2' if the second: ")
                            judgement = int(judgement) #just for type safety
                        correctness = (judgement == 2)
                        result_df = pd.DataFrame({'true_r':[r], 'test_r':[test_r], 'approach':[a], 'correct':[correctness]})
                        #print(result_df.head())
                    else: 
                        play_sound(test_ds)
                        time.sleep(2) #delineate the two beeps
                        winsound.Beep(440, 1000) #beep in middle to show deliniation
                        time.sleep(2)
                        play_sound(true_ds)
                        judgement = -1
                        while (judgement in [1, 2]) == False: #force the user to give a good input
                            judgement = input("which audio had higher correlation? Input '1' if the first, '2' if the second: ")
                            judgement = int(judgement) #just for type safety
                        correctness = (judgement == 1)
                        result_df = pd.DataFrame({'true_r':[r], 'test_r':[test_r], 'approach':[a], 'correct':[correctness]})
                        #print(result_df.head())
                    #post randomization logic
                    exp_df = exp_df.append(result_df, ignore_index = True)
                    if correctness: 
                        print("You got it right!")
                        test_r -= 0.01
                    else: 
                        print("Try again next time...")
                        test_r += 0.03
                    #check flags for impossible values
                    if test_r <= r: #reset if at minimal barrier
                        test_r = r + 0.1
                    if test_r >= 1: #reset if at maximal barrier
                        test_r = r + 0.1
            else: 
                test_r = r - 0.1 #set the test r value
                test_count = 0
                while test_count < 20: 
                    print('count num: ' + str(test_count))
                    test_count += 1
                    (xs, true_ds) = generate_data(r)
                    (xs, test_ds) = generate_data(test_r)
                    flip_flag = random.randint(0,1)
                    if flip_flag == 0:
                        play_sound(true_ds)
                        time.sleep(2) #delineate the two beeps
                        winsound.Beep(440, 1000) #beep in middle to show deliniation
                        time.sleep(2)
                        play_sound(test_ds)
                        judgement = -1
                        while (judgement in [1, 2]) == False: #force the user to give a good input
                            judgement = input("which audio had higher correlation? Input '1' if the first, '2' if the second: ")
                            judgement = int(judgement) #just for type safety
                        correctness = (judgement == 1)
                        result_df = pd.DataFrame({'true_r':[r], 'test_r':[test_r], 'approach':[a], 'correct':[correctness]})
                    else: 
                        play_sound(test_ds)
                        time.sleep(2) #delineate the two beeps
                        winsound.Beep(440, 1000) #beep in middle to show deliniation
                        time.sleep(2)
                        play_sound(true_ds)
                        judgement = -1
                        while (judgement in [1, 2]) == False: #force the user to give a good input
                            judgement = input("which audio had higher correlation? Input '1' if the first, '2' if the second: ")
                            judgement = int(judgement) #just for type safety
                        correctness = (judgement == 2)
                        result_df = pd.DataFrame({'true_r':[r], 'test_r':[test_r], 'approach':[a], 'correct':[correctness]})
                    #print(result_df.head())
                    exp_df = exp_df.append(result_df, ignore_index = True) #add result
                    if correctness: 
                        print("You got it right!")
                        test_r += 0.01
                    else: 
                        print("Try again next time...")
                        test_r -= 0.03
                    #check flags for impossible values
                    if test_r >= r: #reset if at minimal barrier
                        test_r = r - 0.1
                    if test_r <= 0: #reset if at maximal barrier
                        test_r = r - 0.1
    exp_df.to_csv("experiment_results.csv", index = False)
    return exp_df
#run the experiment
sonification_experiment()
