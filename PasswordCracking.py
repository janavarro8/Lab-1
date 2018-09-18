"""
Course: CS2302 Data Structures
Author: Javier Navarro
Assignment: Option C (Password Cracking)
Instructor: Diego Aguirre
TA: Manoj Saha
Last modified: 9/17/18
Purpose: Find passwords to accounts in a given file
"""

import hashlib

def main():
    userName = []       #to hold usernames from file
    saltVal = []        #to hold salt values from file
    hashedPass = []     #to hold hashed passwords from file
    totalMatches = 0    #to hold number of matched passwords
    lowerLim = -1       #lower limit given by user
    upperLim = -1       #upper limit given by user
    
    try:
        with open("password_file.txt", 'r') as file:
            for i in file:
                line = i.strip()
                currLine = line.split(",")
                userName.append(currLine[0])
                saltVal.append(currLine[1])
                hashedPass.append(currLine[2])
    except FileNotFoundError:
        print("File not found. File should be named password_file.txt.")
        print("Ending program.")
        return
    
    while((lowerLim == -1) or (upperLim == -1)): #if no error is caught, the variables will no longer be -1
        try:
            lowerLim = int(input('Enter the smallest size of the password:'))
            upperLim = int(input('Enter the largest size of the password:'))
        except ValueError:
            print("\nNot a number")

    print("Finding passwords...\n")
    
    actualPass = ['No Password Found'] * len(userName)
    thepass = findPass(lowerLim, upperLim, saltVal, hashedPass, actualPass, totalMatches)
    for i in range(len(userName)):
        print(userName[i], " ", thepass[i])

""" Hashes the given string """
def hash_with_sha256(str):
    hash_object = hashlib.sha256(str.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

""" Finds the correct passwords and returns an array aligned with the userName array """
def findPass(lowerLim, upperLim, saltVal, hashedPass, actualPass, totalMatches):
    if((lowerLim > upperLim) or (totalMatches == len(hashedPass))):  #base case                                                                                                                                               return -1
        return actualPass    
    
    zeroes = ['0'] * (lowerLim - 1)      #example lowerLim = 3: zeroes = ['0', '0']
    counter = 0                          #counts to the max value of length lowerLim
    exponent = 1                         #used to check num digits in counter
    
    for i in range(10 ** lowerLim):      #total possible combinations
        if(counter >= (10 ** exponent)): #checks number of digits in counter
            del zeroes[-1]               #removes last index of zeroes
            exponent += 1
        zeroes.append(str(counter))      #adds counter to zeroes list
        tempPass = ''.join(zeroes)       #combines list into a string
        
        for j in range(len(hashedPass)):
            tempHash = hash_with_sha256(tempPass + saltVal[j])
            if(tempHash == hashedPass[j]): #checks if the passwords match
                actualPass[j] = tempPass
                totalMatches += 1
        """ End of inner for loop """
        
        del zeroes[-1]                #delete last index to handle double digits, triple, etc. in counter
        counter += 1
    """ End of outer for loop """
    
    return findPass((lowerLim + 1), upperLim, saltVal, hashedPass, actualPass, totalMatches)
    
main()