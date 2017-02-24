import numpy as np
import random
import time
def chartoind(char):
    if (ord(char) == 32):
        return 0
    if (ord(char) > 64 and ord(char) < 91):
        return ord(char) - 64
    return -1

def indtochar(ind):
    if (ind == 0):
        return ' '
    else:
        return chr(ind+64)

def builddict(filename):    
    probs = np.zeros([27,27])
    f = open(filename, 'r')
    text = f.read()
    text = text.upper()
    length = len(text)
    pointer = 1
    while pointer < length:        
        active = chartoind(text[pointer])
        if (active != -1):
            prev = chartoind(text[pointer-1])
            if (prev != -1):
                probs[prev, active] += 1
        pointer += 1
    probs[0,0] = 0
    for i in range(27):
        rowsum = sum(probs[i,:])
        if rowsum != 0:
            probs[i,:] = probs[i,:] / rowsum
    return probs

def genstring(probs):
    length = random.randint(0,10)+20
    charlist = ' '
    for i in range(length):
        active = chartoind(charlist[i])
        rand = random.random()
        j = 0
        while (j < 27):
            if (rand < probs[active, j]):
                charlist = charlist + indtochar(j)
                break
            else:
                rand = rand - probs[active, j]
                j = j + 1
    return charlist

def builddictzero(filename):
    shape = [27]
    probs = np.zeros(shape)
    f = open(filename, 'r')
    text = f.read()
    text = text.upper()
    length = len(text)
    pointer = 0
    while pointer < length:
        activeind = chartoind(text[pointer])
        if (activeind != -1):            
            probs[activeind] += 1
        pointer += 1    
    return probs

def builddictrange(filename, dist):
    shape = [27]
    for i in range(dist):
        shape.append(27)
    probs = np.zeros(shape)
    f = open(filename, 'r')
    text = f.read()
    text = text.upper()
    length = len(text)
    pointer = dist
    while pointer < length:
        previnds = np.zeros(dist)
        for i in range(dist):
            previnds[i] = chartoind(text[pointer-dist+i])
        activeind = chartoind(text[pointer])
        if (min(previnds)>-1 and activeind != -1):            
            probs[tuple(previnds)][activeind] += 1
        pointer += 1
    probs[0,0] = 0
    
    return probs

def genstringrange(probs, dist):    
    length = random.randint(0,10)+50
    charlist = ''
    start = 0
    for i in range(dist):
        charlist += indtochar(random.randint(0,26))
    i = 0
    while (i < start+length):
        pointer = i+dist
        previnds = np.zeros(dist)
        for j in range(dist):
            previnds[j] = chartoind(charlist[pointer-dist+j])
        previnds = tuple(previnds)
        rowsum = sum(probs[previnds])
        if (rowsum != 0):
            smprobs = probs[previnds]/rowsum
        else:
            start = i
            smprobs = np.ones(27)/27
        rand = random.random()
        j = 0
        while (j < 27):
            if (rand < smprobs[j]):
                charlist = charlist + indtochar(j)
                break
            else:
                rand = rand - smprobs[j]
                j = j + 1
        i += 1
    return charlist[start:]


def cleantext(filename, outfilename):    
    f = open(filename, 'r')
    text = f.read()
    text = text.upper()
    length = len(text)
    pointer = 0
    if (text[0] != ' '):
        isspace = False
    else:
        isspace = True
    if (chartoind(text[0]) != -1):
        newtext = text[0]
    else:
        newtext = ''
    recentremove = 0
    for i in range(length):
        if (text[i] == ' '):
            if (isspace == True):
                newtext += text[recentremove+1:i]
                recentremove = i
            isspace = True
        else:
            if (chartoind(text[i]) == -1):
                newtext += text[recentremove+1:i]
                recentremove = i
            else:
                isspace = False
    f2 = open(outfilename, 'w')
    f2.write(newtext)

def randwords():
    f = open('cleanshakespeare.txt')
    text = f.read()
    words = text.split(' ')
    nwords = len(words)
    start = random.randint(0,nwords-1)
    curstr = words[start]
    line = curstr
    length = random.randint(5,8)
    for i in range(length-1):
        ninstances = words.count(curstr)
        ind = random.randint(0,ninstances-1)
        spl = text.split(curstr)
        curstr = spl[ind].split(' ')[1]
        line += ' ' + curstr
    return line


def randwordsback(root = ''):
    f = open('cleanshakespeare.txt')
    text = f.read()
    words = text.split(' ')
    nwords = len(words)
    if (root == ''):
        start = random.randint(0,nwords-1)
        curstr = words[start]
    else:
        curstr = root
    line = curstr
    length = random.randint(5,8)
    for i in range(length-1):
        ninstances = words.count(curstr)
        ind = random.randint(0,ninstances-1)
        spl = text.split(curstr)
        curstr = spl[ind-1].split(' ')[-2]
        line = curstr + ' ' + line 
    return line

def poem(probs0,probs1, probs2,probs3,probs4,probs5):
    fn = 'shakespeare.txt'
    cl = 'cleanshakespeare.txt'
    cleantext(fn,cl)
    fr = open(cl)
    clt = fr.read()
#    probs0 = builddictzero(cl)
#   probs1 = builddictrange(cl, 1)
#   probs2 = builddictrange(cl, 2)
#    probs3 = builddictrange(cl, 3)
#    probs4 = builddictrange(cl, 4)
#    probs5 = builddictrange(cl, 5)
    text = ''
    text += genstringrange(probs0, 0) + '\n'
    text += genstringrange(probs1, 1) + '\n'
    text += genstringrange(probs2, 2) + '\n'
    text += genstringrange(probs3, 3) + '\n'
    text += genstringrange(probs4, 4) + '\n'
    text += genstringrange(probs5, 5) + '\n'
    line7 = randwords()
    while True:
        var = raw_input("Enter common word that rhymes with " + line7.split(' ')[-2])
        if (clt.count(var.upper())>0):
            break
        else:
            print var + " does not appear in " + fn + ", enter another"
    line8 = randwordsback(var.upper())
    text += line7 + '\n' + line8 + '\n'
    return text
