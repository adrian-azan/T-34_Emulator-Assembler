import copy

memory = []
stack = []
INS = ""
AMOD = ""
PC = 0
AC = 0
XR = 0
YR = 0
SR = [0,0,1,0,0,0,0,0]
SP = 255

def printStep(PC, OPC, INS, AMOD, AC, XR, YR, SP, SR, operand):
    Output = '{:4X}  {:02X}  {:^3}   {:>4} {:^} {:^} {:02X} {:02X} {:02X} {:02X} '.format(PC,int(OPC, base = 16),INS,AMOD, operand[:2], operand[2:] ,int(AC),int(XR),int(YR),int(SP))
    SROutput ="{}{}{}{}{}{}{}{}".format(SR[0], SR[1], SR[2], SR[3], SR[4], SR[5], SR[6], SR[7])
    print(Output + SROutput)

def openFile(fileName):
    if fileName[-2:] != ".o":
        fileName += ".o"

    fin = open(fileName,"r")

    return fin


def checkRegisters(R):
    if R < 0:
        return R + 256
    elif R > 255:
        return R - 256
    return R
  
def negative(R, SR):
    if R >= 0 and R <= 127:
        SR[0] = 0
    else:
        SR[0] = 1

    return SR

def zero(R, SR):
    if R == 256 or R == 0:
        SR[6] = 1
        SR[0] = 0
    else:
        SR[6] = 0

    return SR

def carry(R,SR):
    if R & 128 == 128:
        SR[7] = 1
    else:
        SR[7] = 0

    return SR


for i in range(0,65536):
    memory.append(str(0))

file = input("Enter file name (Press enter if no file): ")
if (file != ''):
    fin = openFile(file)

    fInput = fin.read(3)
    i = 0
    while  fInput != '':
        fInput = fInput.rstrip(' ')
        fInput = fInput.replace("\n", "")
        memory[i] = fInput
        fInput = fin.read(3)
        i += 1



while True:
    userInput = str(input("> "))
    
      

    #Print Range of memory addreses
    if userInput.find('.') != -1:
        count = 0
        total = 0
        memRange = userInput.split('.')
        begi = int(memRange[0], base =16)
        end = int(memRange[1], base =16)
        temp = " {:>4}".format(str(hex(begi)[2:]))
        print(temp , end = '    ')
        for i in range(begi, end):            
            if count == 8:
                temp = "{:>4}".format(str(hex(begi + total)[2:]))
                print('\n', temp, end =  '    ')
                count = 0
            print(memory[i] + '  ', end = '')
            count += 1
            total += 1


    #Edit Memory addresses      
    elif userInput.find(':') != -1:
        start = int(userInput.split(':')[0], base = 16)
        edits = userInput.split(' ')[1:]
        j = 0
        for i in range(start, start+len(edits)):
            memory[i] = edits[j]
            j+=1


    elif userInput[-1:].upper() == 'R':
        stack = []
        INS = ""
        AMOD = ""
        operand = ""
        oldPC= -1
        AC = 0
        XR = 0
        YR = 0
        SR = [0,0,1,0,0,0,0,0]
        SP = 255
        PC = int(userInput[:-1], base = 16)
        flag = True
        print(" PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC")
        while flag:
            OPC = memory[PC].rstrip(' ')
            oldPC= -1
            operand = ""
            if OPC == "90":
                INS = "BCC"
                AMOD = "rela"
                oldPC = PC
                PC = PC + 1
                if (SR[7] == 0):
                    operand = memory[PC]
                    PC = int(operand, base = 16)


            elif OPC == "B0":
                INS = "BCS"
                AMOD = "rela"
                oldPC = PC
                PC = PC + 1
                if (SR[7] == 1):
                    operand = memory[PC]
                    PC = int(operand, base = 16)

            elif OPC == "F0":
                INS = "BEQ"
                AMOD = "rela"
                PC += 1
                oldPC = PC
                
                if (SR[6] == 1):
                    operand = memory[PC]
                    PC = int(operand, base = 16)

            elif OPC == "30":
                INS = "BMI"
                AMOD = "rela"
                PC += 1
                oldPC = PC
                if (SR[0] == 1):
                    operand = memory[PC]
                    PC = int(operand, base = 16)

            elif OPC == "D0":
                INS = "BNE"
                AMOD = "rela"
                PC += 1
                oldPC = PC
                if (SR[6] == 0):
                    operand = memory[PC]
                    PC = int(operand, base = 16)

            elif OPC == "10":
                INS = "BPL"
                AMOD = "rela"
                oldPC = PC
                PC = PC + 1
                if (SR[0] == 0):
                    operand = memory[PC]
                    PC = int(operand, base = 16)

            elif OPC == "50":
                INS = "BVC"
                AMOD = "rela"
                oldPC = PC
                PC = PC + 1
                if (SR[1] == 0):
                    operand = memory[PC]
                    PC = int(operand, base = 16)


            elif OPC == "70":
                INS = "BVS"
                AMOD = "rela"
                oldPC = PC
                PC = PC + 1
                if (SR[1] == 1):
                    operand = memory[PC]
                    PC = int(operand, base = 16)

            elif OPC == "4C":
                INS = "JMP"
                AMOD = "abso"
                oldPC = PC
                PC += 1
                big = memory[PC+1]
                little = memory[PC]
                operand = big + little
                PC = int((big[:2] + little[:2]),base = 16)
                

            
            elif OPC == "20":
                INS = "JSR"
                AMOD = "abso"
                oldPC = PC
                PC += 1
                big = memory[PC+1]
                little = memory[PC]
                PC += 1
                stack.append(PC)
                PC = int((big[:2] + little[:2]),base = 16)
                operand = big + little
                
                SP -= 1

            #NEED JUMP COMMANDS

            elif OPC == "EA":
                INS = "NOP"
                AMOD = "impl"
               
            elif OPC == "0A":
                INS = "ASL"
                AMOD = "A"
                if AC & 128 == 128:
                    SR[7] = 1
                AC = AC << 1
                SR = negative(AC,SR)
                SR = zero(AC,SR)
                SR = carry(AC,SR)

            elif OPC == '18':
                INS = "CLC"
                AMOD = "impl"
                SR[7] = 0

            elif OPC == "D8":
                INS = "CLD"
                AMOD = "impl"
                SR[4] = 0

            elif OPC == "58":
                INS = "CLI"
                AMOD = "impl"
                SR[5] = 0

            elif OPC == "B8":
                INS = "CLV"
                AMOD = "impl"
                SR[1] = 0

            elif OPC == "CA":
                INS = "DEX"
                AMOD = "impl"
                XR -= 1
                SR = negative(XR,SR)
                SR = zero(XR,SR)


            elif OPC == "88":
                INS = "DEY"
                AMOD = "impl"
                YR -= 1
                SR = negative(YR,SR)
                SR = zero(YR,SR)
               

            elif OPC == "E8":
                INS = "INX"
                AMOD = "impl"
                XR += 1
                SR = negative(XR,SR)
                SR = zero(XR, SR)
               

            elif OPC == "C8":
                INS = "INY"
                AMOD = "impl"
                YR += 1
                SR = negative(YR,SR)
                SR = zero(YR, SR)

            elif OPC == "4A":
                INS = "LSR"
                AMOD = "A"
                if AC & 1 == 1:
                    SR[7] = 1
                AC = AC >> 1
                SR = zero(AC,SR)
               
                
                    
                

            elif OPC == "48":
                INS = "PHA"
                AMOD = "impl"
                stack.append(AC)
                SP -= 1
                if SP < 0:
                    print("No More Stack Space")
                    SP += 1
                                                       

            elif OPC == "08":
                INS = "PHP"
                AMOD = "impl"
                stack.append(copy.copy(SR))
                SP -= 1
                if SP < 0:
                    print("No More Stack Space")
                    SP += 1



            elif OPC == "68":
                INS = "PLA"
                AMOD = "impl"
                AC = stack.pop()
                SR = negative(AC,SR)
                SR = zero(AC,SR)
                SP += 1
                if SP > 255:
                    print("Nothing to pull")
                    SP -= 1

            elif OPC == "28":
                INS = "PLP"
                AMOD = "impl"
                SR = stack.pop()
                SP += 1
                if SP > 255:
                    print("Nothing to pull")
                    SP -= 1

            elif OPC == "2A":
                INS = "ROL"
                AMOD = "A"
                SR = carry(AC,SR)
                AC = AC << 1
                SR = negative(AC,SR)
                SR = zero(AC,SR)
                
                if SR[7] == 1:                    
                    AC += 1               
               

            elif OPC == "6A":
                INS = "ROR"
                AMOD = "A"
                temp = AC & 1
                temp = temp << 7
                AC = AC >> 1
                AC = AC | temp
                if temp == 128:
                    SR[7] = 1
                else:
                    SR[7] = 0

                SR = zero(AC,SR)
                SR = negative(AC,SR)

              
            elif OPC == "38":
                INS = "SEC" 
                AMOD = "impl"
                SR[7] = 1

            elif OPC == "F8":
                INS = "SED"
                AMOD = "impl"
                SR[4] = 1

            elif OPC == "78":
                INS = "SEI"
                AMOD = "impl"
                SR[5] = 1

            elif OPC == "AA":
                INS = "TAX"
                AMOD = "impl"
                XR = AC

                SR = negative(XR,SR)
                SR = zero(XR,SR)
                

            elif OPC == "A8":
                INS = "TAY"
                AMOD = "impl"
                YR = AC

                SR = negative(YR,SR)
                SR = zero(YR,SR)

            elif OPC == "BA":
                INS = "TSX"
                AMOD = "impl"
                XR = SP

                SR = negative(XR,SR)
                SR = zero(XR,SR)
              

            elif OPC == "8A":
                INS = "TXA"
                AMOD = "impl"
                AC = XR
                SR = negative(AC,SR)
                SR = zero(AC,SR)
                

            elif OPC == "9A":
                INS = "TXS"
                AMOD = "impl"
                SP = XR
             

            elif OPC == "98":
                INS = "TYA"
                AMOD = "impl"

                AC = YR
                SR = negative(AC,SR)
                SR = zero(AC,SR)
              
                                                                                                                                  
            if OPC == "0" or OPC == "00":
                flag = False
                SR[3] = 1
                SR[5] = 1
                INS = 'BRK'
                SP -= 3
                stack.append(PC)
                stack.append(copy.copy(SR))

            operand = operand.replace(" ", "")
            if (len(operand)  == 2):
                operand += "--"
            elif (len(operand) == 0):
                operand += "--" + "--"
            XR =  checkRegisters(XR)
            YR = checkRegisters(YR)
            AC = checkRegisters(AC)
            SP = checkRegisters(SP)
            if (oldPC != -1):
                printStep(oldPC, OPC, INS, AMOD, str(AC), str(XR), str(YR), str(SP), SR, operand )
            
            else:
                printStep(PC, OPC, INS, AMOD, str(AC), str(XR), str(YR), str(SP), SR, operand)
                PC+= 1

            if flag == False:
                PC += 2


        
    elif int(userInput, base = 16) >= 0 and int(userInput, base = 16) < int(hex(10000), base = 16):
        print(userInput + "\t" + memory[int(userInput, base = 16)])
    
    print("\n\n\n\n")


fin.close()