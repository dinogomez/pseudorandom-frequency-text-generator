# Lyric Generator
# Dino Paul Gomez - SEG31 - 7/24/2021


import os
import re
import math
import random
import time
import json
import statistics
from collections import defaultdict
from typing import final

#GLOBAL VARS
freq = defaultdict(list)
weight = defaultdict(list)
sentence = []

#clear_console function
#Sourced @https://www.delftstack.com/howto/python/python-clear-console/
def clear_console():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

#sleep_print_loop function
#Sourced @Major-Exam2
def sleep_print(file_name,e,s):
        #Prints the error statement @e , @s number of times
        while(s > 0):
            print(f"Error opening file '{file_name}', {e}, {s}s")
            s-=1
            time.sleep(1.1)
            clear_console()

#sanitize function
#santize text for illegal charachters
#referenced from @Sir's naive-lyric-generator source file
#@https://github.com/johnpaulada/naive-lyric-generator/blob/master/main.js
# [START]
def sanitize(text):
    #return text.toLowerCase().replace(/[,\.'"\?\(\)]/g, '')
    text_lower =  text.lower()
    text_strip = text_lower.strip('\=')
    text_clean_special = re.sub('[!@#$%^&*()],', '', text_strip.replace(',','').replace('(','').replace(')',''))
    return text_clean_special

def tokenize(text):
    text_split = text.split()
    return text_split

def get_random_int(min,max):
    min = math.ceil(min)
    max = math.floor(max)
    return math.floor(random.randint(min,max))
# [END]
#get_file_name function
def get_file_name():
    file_name = input("Specify Lyric File: - ")
    return file_name

#get_file function
#Sourced @Major-Exam2
def get_file(file_name):
    #Clear Screen
    clear_console() 
    #Try Catch Verification on File
    try:
        with open(file_name) as f:
            file = open(file_name)
            print(f"\nFile '{file_name}' succesfully loaded")  
            return file
            
    #Recurse Function on Fail
    #Call Sleep Print to Print Error
    except IOError as e:
        clear_console()
        sleep_print(file_name,e,3)
        get_file(file_name)       


#split_file_content function
#split file content into words, store into list
def split_file_content(file):
    file_list = []
    for eachline in file:
        # [DEBUG]
        # print("eachLine:- "+ sanitize(eachline))
        eachline = sanitize(eachline)
        file_list.extend(eachline.split('\n'))
    file_list = [x.strip() for x in file_list if x.strip()]
    return file_list

#store_model function
#persistent saving
def store_model(dict):
    with open('model.json','w') as file:
        json.dump(dict,file)

#train_model function
#Sorting and Weighting of Words
#Pseudo-Random Frequency Model
def train_model(file_content):
    #quantity of words for the chain
    k = 0
    #default dictionary to list
    global freq
    global sentence
    global weight
    words = []
    
    #Separate Lyrics
    for i in range(len(file_content)):
        words = file_content[i].split(' ')
        words = [word for word in words if word != '']
        sentence.append(words)
         #Frequency Sort through 2D array
        #Enter First Array
        for i in range(len(sentence)):
            #Enter Nested Array
            for j in range(len(sentence[i])):
                if j not in freq.keys():
                    #REMOVE DUPLICATES
                    if(sentence[i][j] not in freq[j]):
                        freq[j].append(sentence[i][j])
                        if(j > 0):
                            weight[sentence[i][j-1]].append(sentence[i][j])
                else:
                    if(sentence[i][j] not in freq[j]):
                        freq[j].append(sentence[i][j])
                        if(j > 0):
                            weight[sentence[i][j-1]].append(sentence[i][j])
                        
    
    store_model(freq)


def generate(freq):
    #Get Median from Model Length
    median_freq = math.ceil(statistics.median(range(len(freq))))
    len_frequency = len(freq)
    len_sentence = len(sentence)
    random_sentence_count = get_random_int(20,len_sentence+20)

    print('\n')
    
    for i in range(random_sentence_count):
        rand_word_count = get_random_int(median_freq+2,len_frequency)
        #Holding for Words
        last_string = ""
        for j in range(rand_word_count):
            random_element = get_random_int(0,len(freq[j]))-1
            if(j==0):
                last_string = freq[j][random_element]
                print(last_string, end=" ")
            else:
                try:
                    last_string = random.choice(weight[last_string])
                    print(last_string, end=" ")
                #On Empty Sequence
                except IndexError as e:
                    try:
                        print(random.choice(list(random.choice(weight.values()))), end=" ")
                    except:
                        pass       
        print("\n")

def command_handler():
    print("\n-------------------------------------------------")
    print("\'ADD\' : Add New Song File")
    print("\'RESET\': Reset JSON Model")
    print("\'EXIT\': Exit Program")

    command = input("\nEnter Command: - ")
    if(command.lower() == 'add'):
        return False
    elif(command.lower() == 'reset'):
        os.remove('model.json')
        print("\n'Model.JSON' succesfully removed.", end="\n")
        return False
    elif(command.lower() == 'exit'):
        return True
    else:
        print(f"Invalid Command '{command}, Please Try Again!'")
        command_handler()

def main():
    # file_content = split_file_content(get_file(get_file_name()))
    # #Training the Model
    # train_model(file_content)
    # generate(freq)
    clear_console()
    exit = False
    while(exit != True):
        file_content = split_file_content(get_file(get_file_name()))
        train_model(file_content) 
        generate(freq)  
        exit = command_handler()
    return 0

def load_print():
    clear_console()
    print(f"\nFile 'model.json' does not exist.") 
    print("Loading in 3") 
    time.sleep(1)
    clear_console()
    print(f"\nFile 'model.json' does not exist.") 
    print("Loading in 2") 
    time.sleep(1)
    clear_console()
    print(f"\nFile 'model.json' does not exist.") 
    print("Loading in 1") 
    time.sleep(1)
    

if __name__ == '__main__':
    # try:
    #     with open('model.json') as f:
    #         f = get_file('Model.json')
    #         print(f"\nFile 'model.json' succesfully loaded")  
    #         data = json.load(f)
    #         print(json.dumps(data, indent=4, sort_keys=True))
    #         print("\nLoading Program in 3s")
    #         time.sleep(3)
    # except IOError as e:
    #     load_print()
            

    main()


