import os

def bitStringToString(s):
    return (int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')).decode('utf-8')

def passwordValueCalculation(password, imgRGB):
    passwordValue = 0
    if password == "":
        return 0
    for char in password:
        passwordValue += ord(char) 
    
    passwordValue = passwordValue%len(imgRGB) # normalize passwordValue within the bounds of image pixel length

    return passwordValue

def stringToBinary(s):
    return ''.join(format(ord(char), '08b') for char in s)

def createDirectory(directoryName):
    try:
        os.mkdir(directoryName)
        print(f"Directory '{directoryName}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directoryName}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directoryName}'.")
    except Exception as e:
        print(f"An error occurred: {e}")