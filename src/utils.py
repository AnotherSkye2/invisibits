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
