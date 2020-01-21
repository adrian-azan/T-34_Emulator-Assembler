#Returns line up to comment
def commentCheck(line):
    for i in range(0,len(line)):
        if (line[i] == '*' or line[i] == ';'):
            return line[:i] +'\n'
    return line

def labelCheck(line):
    length = len(line)
    label = ''

    #Max length for a label is 9 spaces
    if (length > 9):
        length = 9

    #Add every letter or number found upto 9th letter to return variable
    for i in range (0, length):
        if line[i].isalnum():
            label += line[i]

    return label
  
def instructionCheck(line):
    length = len(line)
    instruction = ''

    #Maximum length of instruction is 13 spaces
    if (length > 13):
        length = 13

    #Adds any letter found on line between 9-13 to return variable
    for i in range (9, length):
        if line[i].isalpha():
            instruction += line[i]

    return instruction

def operandCheck(line):
    length = len(line)
    operand = ''

    #Maximum length for operand is up to 25th space
    if (length > 25):
        length = 25
    
    #Adds any letter found on line between 14-25 to return variable
    for i in range (14, length):
        if line[i] != ' ' or line[i] != '\n':
            operand += line[i]

    return operand

#Checks for any instructions which dont add to PC Count
def pseudoCheck(instruction):
    pseudoInstructions = ["ORG", "EQU", "END"]
    for i in pseudoInstructions:
        if i == instruction:
            return True

    return False

def impliedCheck(instruction):
    #Implied instructions only need their machine instruction
    #If the instruction was found, it's machine code is returned
    for i in implied:
        if instruction == i:
            return implied[instruction]

    for i in branch:
        if instruction == i:
            return branch[instruction]
    
    return -1

#The following checks use key patterns in the syntax to find the correct 
#machine code. This unfortunately only works with hex syntax as
#other number formats will have varying lengths
def immediateCheck(operand):
    if len(operand) == 3:
        return -4
    elif len(operand) == 5 and ',' in operand:
        return 12
    elif len(operand) == 5:
        return 4
    elif len(operand) == 7 and 'X' in operand and '(' in operand:
        return -8
    elif len (operand) == 7 and 'Y' in operand and '(' in operand:
        return 8
    elif len(operand) == 7 and 'X' in operand:
        return 20
    elif len(operand) == 7 and 'Y' in operand:
        return 16

    elif operand[0] == "#":
        return 0
    elif operand[0].isdigit():
        return 0


    return -100

def immediate3Check(operand):
    if len(operand) == 3:
        return 4
    elif len(operand) == 5:
        return 12
    elif operand[0] == "#":
        return 0
    return -100

def immediate5Check(operand):
    if len(operand) == 3:
        return 4
    elif len(operand) == 5 and ',' in operand:
        return 20
    elif len(operand) == 5:
        return 12
    elif len(operand) == 7:
        return 28
    elif operand[0] == "#":
        return 0
    return -100
   
def zeroCheck(operand):
    if len(operand) == 5 and 'X' in operand:
        return 16
    elif len(operand) == 5 and 'Y' in operand:
        return 20
    elif len(operand) == 5:
        return 8
    elif len(operand) == 7 and 'X' in operand:
        return -4
    elif len(operand) == 7 and 'Y' in operand:
        return 12
    elif len(operand) == 7:
        return 32
    elif len(operand) == 3 or '0x' in operand:
        return 0
    elif operand[0].isdigit():
        return 0
    return -100

def jumpCheck(operand):
    #only jmp should have paranthesis in an operand
    if instruct == "JMP" and operand[0] == "(" and operand[-1] == ")":
           operand = operand[1:-1]
           return 16
    #Returns an error flag if jsr has parantheses
    elif instruct == "JSR" and (operand[0] == "(" or operand[-1] == ")"):
        return -100

    #formats operand if it is in 0x hex format
    if 'x' in operand:
        operand = operand[1:]

    #Throws an error if not 4 bytes
    elif len(operand) != 5:
       return -100 
    return 0
    

def accumCheck(operand):
    if len(operand) == 3:
        return -4
    elif len(operand) == 5 and 'X' in operand:
        return 12
    elif len(operand) == 5:
        return 4
    elif len(operand) == 7:
        return 20

    elif operand == '':
        return 0

    return -100

#Formats the operand to match with the examples outputs
def operandFormat(operand):
    
    op = ''
    #Removes trailing 0x from any hex numbers
    if operand[:2] == '0x':
        operand = operand[2:]
    for i in operand:
        if i.isalnum() and i != ',' and i != 'X' and i != 'Y':
            op += i.upper()
    return op

#Checks all instruction groups for current instruction.
def badOpcode(instruct):
    if (instruct in zeroPage or instruct in jump or instruct in immediate
      or instruct in branch or instruct in implied or instruct in accum
      or instruct in immediate3 or instruct in immediate5 or instruct == "CHK"):
        return False

    return True

def operation(operand):
    new = 0
    if '+' in operand:
        place = operand.find('+')
        one = operand[:place]
        two = operand[place+1:]
        one = symbolTable[one][2:]
        operand = int(one)+int(two)
        return '0x'+ str(operand)
    if '-' in operand:
        place = operand.find('-')
        one = operand[:place]
        two = operand[place+1:]
        one = symbolTable[one][2:]
        operand = int(one)-int(two)
        return '0x'+ str(operand)
    if '*' in operand:
        place = operand.find('*')
        one = operand[:place]
        two = operand[place+1:]
        one = symbolTable[one][2:]
        operand = int(one)+int(two)
        return '0x'* str(operand)

    return operand

#--------------------------------------------------------------------------------------


lineNumber = 1
totalNumBytes = 0
totalErrors = 0
start = 32768

symbolTable = {}
alphabetical = []
numerical = []
machineInstructions = []

implied = {
           'BRK' : 0x00, 'RTI' : 0x40, 'RTS' : 0x60, 'PHP' : 0x08, 'CLC' : 0x18, 
           'PLP' : 0x28, 'SEC' : 0x38, 'PHA' : 0x48, 'CLI' : 0x58, 'PLA' : 0x68,
           'SEI' : 0x78, 'DEY' : 0x88, 'TYA' : 0x98, 'TAY' : 0xA8, 'CLV' : 0xB8,
           'INY' : 0xCB, 'CLD' : 0xD8, 'INX' : 0xE8, 'SED' : 0xF8, 'TXA' : 0x8A,
           'TXS' : 0x9A, 'TAX' : 0xAA, 'TSX' : 0xBA, 'DEX' : 0xCA, 'NOP' : 0xEA,
           }

branch = {
          'BCC' : 0x90,'BCS' : 0xB0,'BEQ' : 0xF0,'BMI' : 0x30,'BNE' : 0xD0,
          'BPL' : 0x10,'BVC' : 0x50,'BVS' : 0x70
          }

accum = {
        'ROL' : 0x2A, 'ROR' : 0x6A, 'ASL' : 0x0A, 'LSR' : 0x4A
        }

zeroPage = {
        'STY' : 0x84, 'STX' : 0x86, 'STA' : 0x85, 'INC' : 0xE6, 'DEC' : 0xC6,
        'BIT' : 0x24    
        }

immediate = {
        'ADC' : 0x69,'AND' : 0x29,'CMP' : 0xC9,'EOR' : 0x49,'LDA' : 0xA9,
        'ORA' : 0x09, 'SBC' : 0xE9
        }

immediate3 = {
        'CPX' : 0xE0, 'CPY' : 0xC0
    }
immediate5 = {
        'LDX' : 0xA2,'LDY' : 0xA0, 
    }

jump = {
    'JMP' : 0x4C , 'JSR' : 0x20
    }
quit = False
while (quit == False):

    fileName = input("File Name: ")
    fin = open(fileName, 'r')
    for line in fin:
        current_line = line.rstrip('\n')
            
        line = commentCheck(current_line)
        label = labelCheck(line)
        instruct = instructionCheck(line)
        operand = operandCheck(line)

        if badOpcode(instruct) == True and instruct != '' and pseudoCheck(instruct) == False:
            print("Bad opcode '" + instruct + "' in line: " + str(lineNumber))
            exit()
    
        elif label in symbolTable:
            print("Duplicate symbol on line: " + str(lineNumber))
            totalErrors += 1
            input("Enter to continue")

        elif len(symbolTable) > 255 or (start + totalNumBytes) > 0xFFFF:
            print("Memory Full")
            exit()

    
        if instruct == "ORG":
            start = int(operand[1:],16)
    
        if label != '' and instruct == 'EQU':
            symbolTable[label] = hex(int(operand[1:],16))
        
        elif label != '' and label not in symbolTable:
            symbolTable[label] = hex(start+totalNumBytes)


        if operand != '' and pseudoCheck(instruct) == False:
            totalNumBytes += 1
        
        if instruct != '' and pseudoCheck(instruct) == False:
            totalNumBytes += 1

        #adds extra byte to any jump instructions
        if instruct in jump:
           totalNumBytes += 1

        lineNumber += 1

   
    #Reset for second pass through file
    totalNumBytes = 0
    lineNumber = 1
    fin.close()
    fin = open(fileName,'r')
    chk = 0

    for line in fin:
        current_line = line.rstrip('\n')
 
        #Change in hex value for different addressing modes
        change = 0
    
        line = commentCheck(current_line)
        label = labelCheck(line)
        instruct = instructionCheck(line)
        operand = operandCheck(line)
        opcode = impliedCheck(instruct)

        operand = operation(operand)
        
        #if the label exists, the operand becomes its hex value
        if operand in symbolTable:
            originalLabel = operand
            operand = symbolTable[operand]

        #If the operand is a label with paraenthesis, parenthesis are removed
        #Not an elegant method but works with jump instructions
        for i in symbolTable:
            if i in operand:
                originalLabel = i
                operand = operand[0] + symbolTable[i] + operand[len(operand)-1]
                break

        #The follwoing if chain checks for what group an instruction is in and if 
        #the base hex has to be adjusted for addressing mode
        if instruct in zeroPage:
           opcode = zeroPage[instruct] 
           change += zeroCheck(operand)
      
        elif instruct in jump:
            change = jumpCheck(operand)
            if '(' in operand:
                operand = operand[1:-1]
            opcode = jump[instruct]    
       

        elif instruct in immediate:
            opcode = immediate[instruct]
            change += immediateCheck(operand)

        elif instruct in immediate3:
            opcode = immediate3[instruct]
            change += immediate3Check(operand)

        elif instruct in immediate5:
            opcode = immediate5[instruct]
            change += immediate5Check(operand)

        elif instruct in branch and originalLabel in symbolTable:
            #Have to fix bad branch. Assuming cant branchmore than a certain amount of bytes away
            opcode = branch[instruct]
            labelPlace = symbolTable[originalLabel]
            #calculates the relative address for a label by subtracting the
            #current byte place from the original label location
            operand = int(labelPlace[2:],16) - (start + totalNumBytes+2)
            #Throws an error if the relative address is greater than 16 bytes away
            #This number can be changed depending on how far away we want a label to be
            if operand < -16 or operand > 16:
                print("Bad branch in line: " + str(lineNumber))
                totalErrors += 1
            #Calculates the negative value if label is behind branch
            if operand < 0:
                operand = 256+operand
            operand = hex(int(operand))

        elif instruct in implied:
            opcode = implied[instruct]

        elif instruct in accum:
            opcode = accum[instruct]
            change += accumCheck(operand)
  
        elif instruct == "CHK":
            opcode = chk
        
        
        if change == -100:
            print("Bad address mode in line: " + str(lineNumber))
            totalErrors += 1
            input("Enter to continue")

        #Adjusts base address based on addressing mode
        opcode += int(change)
        operand = operandFormat(operand)
    

        #Includes trailing zeros for odd length numbered hex codes
        if len(operand) == 3 or len(operand) == 1:
            operand = "0" + operand

        #Puts hex code into big endian format
        if len(operand) == 4:
            operand = operand[2:] + " " + operand[:2]

        #If the line was a comment, prints out nothing but the line
        if opcode == -1:
            print("\t\t" + '%3s' % str(lineNumber) + " " + current_line)
        else:    
            #sets up machine instructions to be outputed to object file
            machine1 = hex(start+totalNumBytes)
            machine2 = format(int(opcode),'#02X')
            machineInstructions.append(machine1[2:].upper() + ": " + (machine2[2:]).upper() + " " + operand)
            #Prints machine instructions and line to screen
            print(machine1[2:].upper() + ": " + 
                  (machine2[2:]).upper() + " " + operand + '\t' + '%3s' % str(lineNumber) + " " + current_line)
        

        if operand != '' and pseudoCheck(instruct) == False:
            totalNumBytes += 1
        if operand != '' and pseudoCheck(instruct) == False and len(operand) == 5:
            totalNumBytes += 1
        
        if instruct != '' and pseudoCheck(instruct) == False:
            totalNumBytes += 1

        #Adds extra byte for jump instructions
        if instruct in jump:
           totalNumBytes += 1

        lineNumber += 1


    fin.close()

    fout = open(fileName[:-2] + ".o", 'w')
    for i in machineInstructions:
        fout.write(i+'\n')

    fout.close()
    numerical = []
    for i in symbolTable:
        #Adds trailing zero to hex number with one digit
        if len(symbolTable[i]) == 3:
            symbolTable[i] = symbolTable[i][:2] + "0" + symbolTable[i][2:]
        numerical.append(symbolTable[i])
        alphabetical.append(i)

    alphabetical.sort()
    numerical.sort()
    print("\n--End assembly, " + str(totalNumBytes) + " bytes, Errors: " + str(totalErrors))
    print('\n\n Symbol table - alphabetical order')

    col = 0
    for i in alphabetical:
        if (col > 3):
            print('\n')
            col = 0
        print(i + "\t=$" + symbolTable[i][2:].upper(), end="\t\t")
        col += 1

    print('\n\n Symbol table - numerical order')
    col = 0
    while len(numerical) > 0:
        for i in symbolTable:
            if col > 3:
                print('\n')
                col = 0
            if symbolTable[i] == numerical[0]:
                 print(i + "\t=$" + symbolTable[i][2:].upper(), end="\t\t")
                 numerical.remove(numerical[0])
                 col += 1
                 break

    print("\n\n\n\n\n")
