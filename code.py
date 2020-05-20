import random 
import string
import re
import numpy as np
import copy
import operator

N = 96
pc = 0.7


class Decoder:
    File = str()
    ListedFile = list()
    pm = 0.07
    Dictionary = str()
    ListedDictionary = list()

    alphabets = string.ascii_lowercase
    punctuations = string.punctuation + "0123456789"
    
    def __init__ (self,File):

        self.UnusedFile = copy.deepcopy(File)
        self.File = File
        for p in self.punctuations:
            self.File = self.File.replace(p, ' ')
        self.File = re.sub(' +', ' ', self.File)
        self.File = self.File.lower()
        self.ListedFile = self.File.split()
        self.ListedFile = list(dict.fromkeys(self.ListedFile))
        self.DicSize = len(self.ListedFile)

        

        self.Dictionary = open("global_text.txt").read()
        for p in self.punctuations:
            self.Dictionary = self.Dictionary.replace(p, ' ')
        self.Dictionary = re.sub(' +', ' ', self.Dictionary)
        self.Dictionary = self.Dictionary.lower()
        self.ListedDictionary = self.Dictionary.split()
        self.ListedDictionary = list(dict.fromkeys(self.ListedDictionary))


    def createPop(self):
        alphabetDict = dict()
        index = 0
        while len(alphabetDict) < 26:
            rnd = random.randint(0,25)
            if self.alphabets[rnd] in alphabetDict:
                continue
            alphabetDict[self.alphabets[rnd]] = self.alphabets[index]
            index += 1
        
        return alphabetDict
    
    def calculateFitness(self,chromosome,count):
        
        fitness = 0
        for i in range(len(self.ListedFile)):
            word = self.ListedFile[i]
            decodedWord = ''
            for ch in word:
                decodedWord += chromosome[ch]
            if(decodedWord in self.ListedDictionary):
                fitness += 1
                
        count += fitness
        return[fitness,count]



    def chooseParents(self,currentPopulation,weights):
        
        sorted_weights = sorted(weights.items(), key=operator.itemgetter(1))
        Parents = []

        for i in range(N-1,int((N/4) * 3 - 1), -1):
            Parents.append(currentPopulation[sorted_weights[i][0]])

        for i in range(0, int(N/4), 2):
            t = self.produceChildren(Parents[i],Parents[i+1])
            Parents += t

        for i in range(0, int(N/2), 2):
            t = self.produceChildren(Parents[i],Parents[i+1])
            Parents += t

        
        return Parents

        
    def produceChildren(self,Parent1,Parent2):
        
        Child1 = copy.deepcopy(Parent1)
        Child2 = copy.deepcopy(Parent2)
        for i in range(7):
            ind = random.randint(0,25)
            temp1 = Child1[self.alphabets[ind]]
            Child1[self.alphabets[ind]] = Parent2[self.alphabets[ind]]
            temp2 = Child2[self.alphabets[ind]]
            Child2[self.alphabets[ind]] = Parent1[self.alphabets[ind]]
            for x in Child1:
                if (Child1[x] == Child1[self.alphabets[ind]]) and (x != self.alphabets[ind]):
                    Child1[x] = temp1

            for x in Child2:
                if (Child2[x] == Child2[self.alphabets[ind]]) and (x != self.alphabets[ind]):
                    Child2[x] = temp2

        return [Child1,Child2]



    def decode(self):
        t = 0
        firstPopulation = []
        for i in range(N):
            chromosome = self.createPop()
            firstPopulation.append(chromosome)

        currentPopulation = firstPopulation
        
        while(1):
            t += 1
            if(t > 175):
                self.pm = 0.5
            Fitness = []
            count = 0
            for i in range(N):
                chromosome = currentPopulation[i]
                temp = self.calculateFitness(chromosome,count)
                chromosomeFitness = temp[0]

                if(chromosomeFitness == self.DicSize):
                    transalphabets = ''
                    for i in range(0,len(self.alphabets)):
                       transalphabets += chromosome[self.alphabets[i]]
                    decoded = self.UnusedFile.translate(str.maketrans(string.ascii_lowercase + string.ascii_uppercase,transalphabets + transalphabets.upper()))
                    return decoded

                Fitness.append(chromosomeFitness)
                count = temp[1]


            weights = dict()
            weights.update([(i,Fitness[i]/count) for i in range(0,N)])
            newPopulation = self.chooseParents(currentPopulation,weights)
            random.shuffle(newPopulation)
            currentPopulation = []

            for i in range(0, N, 2):
                probability = random.random()
                if(probability < pc):
                    newChildren = self.produceChildren(newPopulation[i],newPopulation[i+1])
                else:
                    newChildren = [newPopulation[i],newPopulation[i+1]]

                for i in range(0,5):
                    probability3 = random.random()
                    if(probability3 < self.pm):
                        first = random.randint(0,25)
                        second = random.randint(0,25)
                        
                        temp = newChildren[0][self.alphabets[first]]
                        newChildren[0][self.alphabets[first]] = newChildren[0][self.alphabets[second]]
                        newChildren[0][self.alphabets[second]] = temp

                        temp = newChildren[1][self.alphabets[first]]
                        newChildren[1][self.alphabets[first]] = newChildren[1][self.alphabets[second]]
                        newChildren[1][self.alphabets[second]] = temp

                currentPopulation += newChildren




                
            
            




