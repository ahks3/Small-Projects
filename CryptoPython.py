#This project is based on the Udemy Course 'Cryptography and Hashing Fundamentals in Python and Java' by, 'Holczer Balazs'. The program is a mix of my own implementations and learning with the mathematical/programming concepts taught in Balazs' course.

k = '[+]' # For readability
cryptoSystem = None #Init Selection Var

while cryptoSystem not in [1,2]: #Present User with Menu, cryptosystem choices, ensure user chooses valid menu item
        try:
            cryptoSystem = int(input(k+"Input crypto option\n1=Caeser Cipher\n2=Viginere Cipher\n"))
        except ValueError:
            print(k+"Syntax - integer from menu\n")
            


if cryptoSystem == 1: #Caeser Cipher
    passKey = None #Init key
    plainText = None #Init plaintext
    while passKey == None: #Check to ensure user presents valid Integer key
        try:
            passKey = int(input(k+"Input Caeser Cipher Key\n"))
        except ValueError:
            print(k+"Syntax - integer key\n")
       
    
    #plainText = input(k+"Enter plaintext\n").replace(" ", "") #for user entry

    plainText = "While in her teens, Doncieux began work as a model. She met Monet, seven years her senior, in 1865 and became his model posing for numerous paintings. They lived together in poverty at the beginning of his career. His aunt and father did not approve of the relationship with Camille. ".replace(" ", "") #for longer paragraph text entry purposes, removing whitepsace helps with frequency analysis
    
    Alphabet = '1QAZ!2WSX@3EDC#4RFV45TGB%6YHN^7UJM&8IK<*,9OL>(.0P:?);/_{"-[+}|=]' #list of all characters expected in plaintext without importing an ASCII module
    
    def detectEnglish():
        None
        

    def caeserEncrypt(plainText, key): #necryption function

        cipherText = '' 

        for c in plainText: #Find character in plaintext as it corresponds to Alphabet position and shift the character, append shifted char to Ciphertext
            index = Alphabet.find(c)
            index = (index + key) % len(Alphabet)
            cipherText += Alphabet[index]
        
        return cipherText

    def caeserDecrypt(cipherText, key):
    
        plainText = ''
    
        for c in cipherText:
            index = ((Alphabet.find(c)) - key) % len(Alphabet)
            plainText+= Alphabet[index]
        
        return plainText

    cipherText = caeserEncrypt(plainText, passKey)
    print(k+cipherText)

    finalPlainText = caeserDecrypt(cipherText, passKey)
    print(k+finalPlainText)

    if input(k+"Crack via bruteforce?\n").lower() not in ['yes', 'y', 'ye']:
        print(k+"Exiting\n")
    else:
        print(k+"Cracking!\n")
        for i in range(len(Alphabet)):
            crackAttempt = ''
            for char in cipherText:
                index = (Alphabet.find(char) + i) % len(Alphabet)
                foundKey = (Alphabet.find(char) - index) % len(Alphabet)
                crackAttempt+= Alphabet[index]
         
            print("Key = ",foundKey," = ",crackAttempt) 
            
    if input(k+"Crack via Frequency Analysis?\n").lower() not in ['yes', 'y', 'ye']:
        print(k+"Exiting\n")
    else:
        def frequencyAnalysis(text):
            text = text.upper()
            letterFreq = {}
            
            #initialize the dictionary with 0 values
            for letter in Alphabet:
                letterFreq[letter] = 0
             
            #considers text to analyze
            for letter in text:
                if letter in Alphabet:
                    letterFreq[letter] += 1
                    
            return letterFreq
        
        def freqCrack(cipherText):
         
            freq = frequencyAnalysis(cipherText)
            freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
            commonChars = ['A', 'E', 'I', 'O', 'T']
            print(freq,"\n")
            for i in range(len(commonChars)):
                print("A possible key value: ", (Alphabet.find(freq[i][0]) - Alphabet.find(commonChars[i])))
            
        freqCrack(cipherText)
            
       
            
            
       
            



            
