
from pass_one import DIRECTIVES, SYMTAB, OPTAB, ERRCTR, PRGLTH, ADDSTA


INTERMEDIATE = open("Intermediatefile.mdt", "r")


OBJ_FILE = open("ObjectFile.obj", "w+")
LISTFILE = open("ListingFile.lst", "w+")
ERRORS = open("errors_file.txt", "w+")


LISTARR = []  
ADDARR = []   
f = ""
f1 = ""



if ERRCTR == 0:
    while True:
        line = INTERMEDIATE.readline()  
        if not line:  
            break

        currentLine = line

        ADDRESS = currentLine[0:8].strip()     
        LABEL = currentLine[9:17].strip()      
        MNEMONIC = currentLine[18:25].strip()  
        OPERAND = currentLine[25:34].strip()   

        if MNEMONIC != "START":  # if there is a duplicate
            ADDARR.append(ADDRESS)

        
        if MNEMONIC == "START":
            OBJ_FILE.write("H^" + LABEL + "^00" + currentLine[0:5].strip().upper() + "^00" + PRGLTH.upper())

            ADDARR.append(currentLine[0:6].strip())
            LISTARR.append("")      

        elif MNEMONIC == "END":
            LISTARR.append("")      

        else:  
            if MNEMONIC in DIRECTIVES or MNEMONIC in OPTAB.keys():
                if MNEMONIC == "RSUB":
                    objCode = OPTAB[MNEMONIC] + "0000"  

                    LISTARR.append(objCode)
                    LISTFILE.write(objCode + "\n")  

                elif MNEMONIC not in DIRECTIVES and ",X" not in OPERAND:  
                    if OPERAND in SYMTAB.keys():
                        LISTFILE.write(OPTAB[MNEMONIC] + SYMTAB[OPERAND] + "\n")  
                        LISTARR.append(OPTAB[MNEMONIC] + SYMTAB[OPERAND])
                        

                elif OPERAND[-2:] == ",X":  
                    if OPERAND[:-2] in SYMTAB.keys():  
                        hexCode = hex(int(bin(1)[-1:] + "00" + bin(int(SYMTAB[OPERAND[:-2]][0:1]))[2:]))[-1:]
                        objCode = OPTAB[MNEMONIC[0:]] + hexCode + (SYMTAB[OPERAND[:-2]][1] +
                                  SYMTAB[OPERAND[:-2]][2] + SYMTAB[OPERAND[:-2]][3])

                        LISTFILE.write(objCode + "\n")
                        LISTARR.append(objCode)

                elif MNEMONIC == "RESW" or MNEMONIC == "RESB" :  
                    LISTARR.append("")

                elif MNEMONIC == "WORD":  
                    objCode = str(hex(int(OPERAND)))[2:]

                    if len(objCode) < 6:  
                        for i in range(6 - len(objCode)):
                            objCode = "0" + objCode

                    LISTFILE.write(objCode + "\n")
                    LISTARR.append(objCode)

                elif MNEMONIC == "BYTE" :  
                    temp = OPERAND[2:len(OPERAND) - 1] 
                    objCode="" 

                    if "X'" in OPERAND:  
                        LISTFILE.write(temp + "\n")  
                        LISTARR.append(temp)

                    elif "C'" in OPERAND:  
                        for i in temp:     
                            hexCode = hex(ord(i))[2:]  
                            LISTFILE.write(str(hexCode))  
                            objCode += hexCode

                        LISTARR.append(objCode + "\n")

            else:
                LISTARR.append("")

else:
    ERRORS.write("Cannot execute pass 2. The input file has errors!")
    print("Cannot execute pass 2. The input file has errors!")

# Writing to object program
currentListing = 1

while currentListing < len(LISTARR):  

    currentAddress = ADDARR[currentListing]
    lngth = 0  # To calc length of record

    if LISTARR[currentListing] != "":
        # Text Record
        OBJ_FILE.write("\nT^00" + currentAddress.upper() + "^")
        pointer = OBJ_FILE.tell()   # save current position of the file object
        OBJ_FILE.write("  ")
        j = currentListing
        while j < len(LISTARR) and LISTARR[j] != "" and lngth <= 9:
            OBJ_FILE.write("^" + LISTARR[j].upper())
            lngth += 1
            j += 1

        currentListing = j - 1

        OBJ_FILE.seek(pointer)  
        tempAdd = hex(int(str(int(ADDARR[currentListing], 16) - int(currentAddress, 16) + int(3))))[2:4]

        if len(tempAdd) == 1:
            tempAdd = "0" + tempAdd 

        if tempAdd == "03":
            tempAdd = "01"

        OBJ_FILE.write(tempAdd.upper())
        OBJ_FILE.seek(0, 2)  

    currentListing += 1

OBJ_FILE.write("\n" + "E" + "^00" + str(hex(ADDSTA))[2:])
OBJ_FILE.close()
INTERMEDIATE.close()
LISTFILE.close()