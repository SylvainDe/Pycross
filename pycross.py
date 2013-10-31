#!/usr/bin/python
from profilehooks import profile, coverage, timecall
from copy import deepcopy

preventGenerationOfUselessCombinations = True
useFuelToKnowWhenChangeHasBeenDone = True 
stopGenerationAsSoonAsPossible = True
maxLevelOfHypothesis = 0 

def match(suff, line):
    assert(len(suff) <= len(line))
    for cS,cL in zip(suff, line):
        assert (cS in [True, False] and cL in [None, True, False])
        if cL is not None and cL!=cS:
            return False
    return True

def generateMatchingComb(rule, line):
    l=len(line)
    if not rule:
        allFalse = [False] * l
        return [allFalse] if match(allFalse, line) else []
    if stopGenerationAsSoonAsPossible:
        l_min = sum(rule)+len(rule)-1
        if l<l_min:
            return []
        elif l==l_min:
            sol=generateSmallestComb(rule)
            assert(len(sol)==l_min)
            return [sol] if match(sol, line) else []
    block = rule[0]
    assert(block>0)
    lastPos = l-block
    if lastPos<0:
        return [] 
    # Try to place the first block in every position, including the end of the line 
    # If it matches the original line, try to place the rest of the blocks on the rest of the line
    comb=[]
    for suff in [ [False]*pos + [True]*block + [False] for pos in range(0, lastPos)] + [ [False]*lastPos + [True]*block ]:
        if match(suff, line): 
            comb.extend([suff+c for c in generateMatchingComb(rule[1:],line[len(suff):])])
    for c in comb:
        assert(len(c) == l and match(c,line))
    return comb 

def generateSmallestComb(rule):
    res=[] # TODO : There must be a way to one-line this and the next 2 lines
    for i,block in enumerate(rule):
        res = res + ([False] if i else []) + [True]*block
    return res

def getExtremeCombinations(rule, l):
    res=[] # TODO : There must be a way to one-line this and the next 2 lines
    for i,block in enumerate(rule):
        res = res + ([0] if i else []) + [i+1]*block
    delta=l-len(res)
    assert(delta>=0)
    return (res+[0]*delta, [0]*delta+res)

class Picross:
    @classmethod
    def problem1(cls): # Solution is obvious 
        return cls.fromProblem([[1],[3],[1,1],[3],[3],[1],[1],[2]], [[],[],[],[],[],[1],[5],[2,1],[3],[2],[2],[],[]])
    @classmethod
    def problem2(cls): # Solution is obvious 
        return cls.fromProblem([[2],[1,1],[4],[2,1],[3,1],[8],[8],[7],[5],[3]], [[1],[2],[1,6],[9],[6],[5],[5],[4],[3],[4]])
    @classmethod
    def problem3(cls): # Solution is NOT obvious 
        return cls.fromProblem([[3],[5],[3,1],[2,1],[3,3,4],[2,2,7],[6,1,1],[4,2,2],[1,1],[3,1],[6],[2,7],[6,3,1],[1,2,2,1,1],[4,1,1,3],[4,2,2],[3,3,1],[3,3],[3],[2,1]], [[2],[1,2],[2,3],[2,3],[3,1,1],[2,1,1],[1,1,1,2,2],[1,1,3,1,3],[2,6,4],[3,3,9,1],[5,3,2],[3,1,2,2],[2,1,7],[3,3,2],[2,4],[2,1,2],[2,2,1],[2,2],[1],[1]])
    @classmethod
    def problem4(cls): # Solution is obvious 
        return cls.fromProblem([[1,4,4,1],[1,1,3,1,1],[1,1,1,1,1],[1,5,1],[9],[11],[4,3,4],[4,3,4],[4,3,4],[11],[9],[7],[5],[3],[1]],[[],[1,2,3],[1,5],[1,1,7],[2,8],[1,3,4],[2,11],[14],[2,11],[1,3,4],[2,8],[1,1,7],[1,5],[1,2,3],[]])
    @classmethod
    def problem5(cls): # Solution is obvious 
        return cls.fromProblem([[],[18],[7,6],[5,5,4],[3,9,3],[1,4,5,2],[1,5,2,1,2],[2,4,2,2,1],[1,2,6,2,1],[1,1,2,7,1,1],[1,3,5,1,1],[2,2,1,1],[1,1,1,2,1],[1,5,2,1],[2,5,2,2,2],[3,5,1,2,2],[4,4,3],[6,5],[18]],[[],[18],[4,1,1,5],[4,1,2,2,4],[3,4,2,2,3],[3,3,3,3,2],[2,7,4,2],[2,5,4,1],[1,2,2,3,1],[1,2,3,2,1],[1,2,1,3,1,1],[1,8,1,1],[1,3,1,2,2,1],[2,2,2,1],[2,2,1,2,2],[3,4,4,2],[4,7,3],[6,5],[18],[]])
    @classmethod
    def problem6(cls): # Solution is obvious
        return cls.fromProblem([[9,9],[8,2,8],[1,5,2,5,1],[2,5,5,2],[2,4,4,2],[1,1,4,1,1],[3,1,3,3,1,3],[4,2,2,2,4],[4,1,6,1,4],[2,2,1,2,1,2,2],[1,1,1,2,2,2,1,1,1],[2,1,2,2,2,1,2],[3,2,6,2,3],[4,1,6,1,4],[3,2,2,2,3],[2,2,3,3,2,2],[2,1,4,1,2],[8,8],[8,2,8],[9,9]],[[3,15],[2,2,4,9],[2,2,3,1,3,3],[3,2,1,1,3],[5,1,4,1,3],[6,3,3,4],[5,2,2,2,3],[5,1,6,1,3],[1,1,2,1,2,2,1],[2,1,8,1,1],[2,1,8,1,1],[1,1,2,1,2,2,1],[5,1,6,1,3],[5,2,2,2,3],[6,3,3,4],[5,1,4,1,3],[3,2,1,1,3],[2,2,3,1,3,3],[2,2,4,9],[3,15]])
    @classmethod
    def problem7(cls): # Multiple solution ? 
        return cls.fromProblem([[],[],[1],[],[1,1],[1,1],[1,1],[],[1],[],[],[1],[1,2],[2,3,2,1],[3,1,4],[4,1,4],[5,1,3],[6,1,2],[7,2,2],[20]],[[1],[2],[3],[4],[5],[6],[7],[8],[1],[1],[1],[1,1],[2,2],[9],[1],[1,1],[3,1],[1,1,7],[1,1,1,6],[1,1,4,1]])
    @classmethod
    def problem8(cls): # Solution is obvious
        return cls.fromProblem([[5,2,9],[4,2,2,4,2],[3,1,1,3,2],[2,1,1,6],[1,1,1,5],[1,1,4],[1,8,1,1,1],[1,2,4,2,1,3],[2,2,2,2,2,4],[1,1,2,2,2,1,5],[1,2,4,1,6],[1,1,2,2,1,1,3],[1,1,1,2,1,1,5],[1,1,1,2,1,1,5],[2,1,1,2,1,1,6],[2,1,1,2,1,1,6],[2,1,2,2,1,4,1],[3,1,2,1,7],[4,6,8],[14,4]],[[5,2,11],[4,1,1,6],[3,1,7,3],[2,1,1,1,3,2],[1,1,1,2,1,1,1],[1,1,2,6,2],[1,2,1,1,2],[1,5,4,3],[1,5,4,3],[1,2,1,1,2],[1,1,2,6,2],[1,1,1,2,1,1,1],[2,1,1,1,3,2],[3,1,3,3,3],[4,1,1,1,5],[5,2,10],[1,3,3,8],[1,17],[6,9,3],[20]])
    @classmethod
    def problem9(cls): # Solution is obvious
        return cls.fromProblem([[20],[1,3,5],[1,4,4],[3,8,3],[1,1,10,2],[1,1,13,1],[1,1,14],[1,1,9,1,2],[1,7,1,3],[1,7,1,3],[1,1,15],[1,1,15],[1,1,14],[1,1,12],[3,10],[1,6,1],[1,1,1,4,1,1],[5,2,1,1,2,1],[6,3,3,2],[7,2,3]],[[2,10,4],[1,1,1,3],[1,1,3,3,1,3],[1,1,1,3],[2,4,4,4],[3,3,3,2],[2,10,3,1],[1,12,2],[1,12,1],[1,14,1],[1,16],[1,15,1],[1,15,1],[1,4,8],[1,13,1],[2,3,5,1],[3,10,2],[4,8,3,1],[5,4,2],[6,4]])
    @classmethod
    def problem10(cls): # Solution is obvious
        return cls.fromProblem([[],[1,1],[2,2],[3,3],[3,3],[5],[1],[1],[7],[7],[1,3],[1,3]],[[],[],[3,2],[5,4],[3,2],[7],[3,4],[5,4],[3,2],[],[],[]])
    @classmethod
    def problem11(cls): # Solution is obvious
        return cls.fromProblem([[4,4],[2,3,3],[2,1,2],[1,1,1,1],[2,2],[6,7],[5,11],[3,3,7,1],[2,7,4],[2,6,3],[3,9,1],[14,4],[22],[20],[17]],[[4],[7],[8],[3,4],[2,4],[2,4],[1,5],[6],[7],[7],[8],[2,9],[2,9],[2,2,1,5],[1,4,5],[1,3,4],[2,3,3],[3,3,3],[2,3,3],[1,3,3],[2,3,3],[3,1,1,3],[3,3,3],[2,2],[3]])
    @classmethod
    def problem12(cls): # Solution is obvious
        return cls.fromProblem([[4],[3],[3],[3],[3],[3],[3],[3],[4]],[[],[3],[5],[7],[3,3],[2,2],[1,1],[1,1],[]])
    @classmethod
    def problem13(cls): # Solution is obvious
        return cls.fromProblem([[4],[6],[8],[8],[9],[9],[9],[9],[8],[11],[12],[14],[17],[17],[3,13],[4,15],[3,17,2],[2,10,9],[3,10,7],[4,11,4],[4,10],[2,11],[11],[11],[11],[12],[11],[11],[12],[12],[13],[12],[5,5],[4,7],[13],[12],[10],[4],[3],[]],[[3],[4],[6,7],[7,11],[5,15],[5,16],[3,12,3],[4,13,3],[4,17,4],[23,4],[23,4],[28],[6,27],[35],[35],[24,1,1,1],[22],[20],[16],[8,5],[5,6],[5],[4],[4],[4],[3],[4],[3],[1]])
    @classmethod
    def problem14(cls): # Solution is obvious
        return cls.fromProblem([[5],[2,4],[2,2,1],[1,2,1],[2,1,1,2],[2,1,1],[2,1,1,1],[2,1,4,1,16],[1,2,2],[1,1,2],[1,2,2],[5,2],[1,2,2,2],[3,3,3],[4,5,4],[2,3,1,2,5],[2,10,6],[2,4],[3,1,3,4],[5,1,4,2],[5,1,1,1,1,1,3,1,1],[7,1,1,1,1,5,2],[8,1,1,1,8,1,1],[10,1,10,3],[22,1,3,1],[23,1,2],[22,1,4],[23,1,4],[30],[30]],[[1,7],[1,9],[10],[6,11],[3,2,12],[4,5,12],[2,2,20],[2,5,7,1,9],[1,2,1,2,1,1,8],[3,1,2,2,1,1,7],[2,1,3,1,1,1,6],[2,1,1,2,2,1,7],[6,2,1,1,1,6],[2,1,1,7],[1,2,1,1,8],[1,2,1,1,7],[1,3,1,8],[1,1,1,9],[1,3,10],[1,3,10],[1,2,10],[1,2,9],[1,3,2,1,3],[1,2,1,1,1,2],[1,1,2,1,3],[1,2,2,1,1,2],[1,3,1,6],[1,4,1,8],[1,5,2,1,1,4],[1,5,6,3]])
    @classmethod
    def problem15(cls): # Test
        return cls.fromProblem([[3,5,4],[6,2,12],[6,5,3,4],[10,14],[3,1,1,7,1],[5,1,7,1],[5,3,3,4,1,2],[5,3,3,3,4],[5,6,4,7],[1,10,4,1,1,5],[1,1,3,1,1,3,6],[3,5,1,2,5],[3,5,1,2,3,4],[4,3,3,3],[3,3,3,1,1,1,4],[1,2,7,3,2,1],[3,2,7,3,1,5],[6,1,14],[6,2,4,1,7,1],[6,3,4,2,3,1],[6,5,1],[5,1,1,1,3,2],[1,1,1],[2,2],[1,2,4,1],[2,3,4,6],[4,2,3,5],[4,2,2,3,3],[1,1],[3,1,2,1]],[[11,7,4],[9,2,8,3],[13,6,2],[4,5,1,5,4],[3,5,5,1,1],[3,1,7,1],[1,5,3],[1,7,2],[1,1,6,4,3],[3,3,3,1,4,1],[1,11,3,1],[2,4,3,1,1],[6,3,3,2,1,1],[4,3,1],[2,2,6],[2,1,1,6,3],[6,1,2,4,1,1],[10,1,2,1,1],[9,2,1,4,1],[2,6,1,5,6],[2,3,3,3,1,3],[7,2,8],[14,3],[3,3,3,3,1,1],[9,1,3,2],[4,7,1,3],[14,1,3],[8,1,1,3],[7,1,1,3],[2,3,2,2,4]])
    @classmethod
    def problem16(cls):
        return cls.fromProblem([[15],[4,5],[2,4],[1,3],[2],[2],[2,4,3],[2,6,2],[2,1,6,2],[2,1,1,4,2],[1,1],[1,3,2,1],[2,2,1,2,1],[3,3,2,1],[9]],[[4,4],[3,1,2,3],[2,1,2,2],[2,1,1],[1,4,2],[1,3],[1,8],[1,3,1,1],[1,4,2,1],[1,4],[2,4,3],[3,3,3],[4,1],[10,3],[10]])
    @classmethod
    def problem17(cls):
        return cls.fromProblem([[8,29,4],[6,4,25,4,3],[5,3,2,3,9,4,2,1,3],[4,2,2,2,2,1,2,2],[4,1,1,9,10,2,2,1],[3,2,6,5,5,1,1],[3,1,5,5,1,1],[3,1,4,4,1,1],[3,1,4,4,1,1],[3,1,3,3,1,1],[3,1,3,6,2],[3,1,2,3,2,4,2],[4,3,1,8,7,1,2,3],[4,2,1,12,11,1,2,4],[5,1,2,7,2,2,6,1,1,4],[4,1,1,1,6,2,2,6,1,2,1,3],[4,1,1,2,4,3,4,3,1,1,1,1,3],[4,1,1,2,1,4,1,2,3,2,1,2,2],[3,1,1,1,2,5,6,1,1,1,3,2],[3,2,1,1,2,1,5,4,4,2,1,2,1,2],[3,2,2,1,1,4,2,2,3,1,1,2,1,1,2],[3,1,3,2,1,1,4,1,5,3,2,1,3,1,2],[3,1,2,1,2,1,3,7,4,1,4,2,2],[2,1,4,1,1,1,2,6,2,2,2,3,2,1],[2,2,4,1,2,1,2,5,2,1,1,3,2,1],[2,2,1,4,1,1,3,3,2,1,4,4,1],[2,3,3,2,1,3,3,7,4,1],[2,3,2,4,5,8,1,2,1],[1,1,3,11,6,7,1,3,1],[1,1,2,2,13,10,2,3,2],[1,2,3,1,6,1,1,7,1,5,2],[1,1,3,2,6,1,1,1,1,4,1,4,2],[1,1,6,7,2,4,2,5,6,1],[1,1,2,3,1,4,2,2,11,2,1],[1,1,1,1,2,1,5,10,1,1,1],[1,1,1,1,4,7,4,10,1,1,1],[1,2,1,1,28,1,1,3],[1,2,1,2,27,2,1,3],[1,1,1,1,26,1,1,1,1],[2,3,1,28,2,1,2,1]],[[40],[28,1],[23,8],[5,6,7,4],[3,6,1,9,3,1],[2,3,2,5,4,2,2],[1,2,4,1,2,5,2],[1,1,4,9,2,3,2],[2,4,2,6,1,4,3],[1,4,1,3,4,1,6],[1,4,3,2,3,5,5],[2,4,1,2,3,4,1,3],[1,2,3,4,2,2,4,4,1],[1,1,2,3,2,1,4,2,4],[2,3,5,3,3,5,4],[3,1,6,1,2,5,5],[3,2,6,2,15],[3,1,8,2,13],[2,2,4,5,15],[2,2,2,2,22],[2,1,1,1,12,6],[2,1,10,4,5],[3,1,3,1,2,4],[3,1,1,4,3,1,4],[3,2,2,3,2,2,5],[3,1,1,5,1,1,5],[3,1,1,5,1,1,5],[3,1,1,5,1,1,5],[3,2,5,2,1,1,4],[3,1,1,3,2,2,4],[3,1,6,4,5],[2,2,12,2,6],[2,2,1,1,22],[2,1,2,2,5,15],[3,1,4,3,2,14],[3,1,7,2,1,13],[3,2,6,1,1,6,8],[3,2,5,2,2,4,7],[2,1,2,4,1,1,1,4,1,4,2],[1,1,4,4,3,1,4,5,1],[1,1,5,1,1,2,1,2,2,3,2],[1,5,2,2,1,5,5,3],[1,6,2,1,4,2,6,1],[1,6,2,6,5,2],[1,5,3,1,9,2],[2,2,4,2,6,3],[1,2,2,2,9,2,1],[3,5,5,8,4],[4,13,9],[27,2]])
    @classmethod
    def easyProblems(cls):
        return [cls.problem1(), cls.problem2(), cls.problem4(), cls.problem5(), cls.problem6(), cls.problem8(), cls.problem9(), cls.problem10(), cls.problem11(), cls.problem12(), cls.problem13(), cls.problem14(), cls.problem15(), cls.problem16()]
    @classmethod
    def hardProblems(cls):
        return [cls.problem3(), cls.problem7()]
    @classmethod
    def newProblems(cls):
        return [cls.problem15()]
    @classmethod
    def fromProblem(cls, rows, cols):
        return cls(rows, cols, [list(i) for i in [[None]*len(cols)]*len(rows)])

    def __init__(self, rows, cols, grid):
        assert(sum([sum(l) for l in rows]) == sum([sum(l) for l in cols]))
        assert(min([min(l) for l in (rows+cols) if l])>0)
        self.rows=rows
        self.cols=cols
        self.grid=grid
        self.rowFuel = [True] * len(self.cols)
        self.colFuel = [True] * len(self.rows)

    def __str__(self): #TODO : This should return a string and not print it but he...
        labelLines=[' '.join(str(n) for n in l) for l in self.rows]
        indent=max([len(s) for s in labelLines])
        nbLines = max([len(l) for l in self.cols])
        for i in range(nbLines):
            print ' ' * indent + '|' + ' '.join([str(l[i+len(l)-nbLines]) if i+len(l)-nbLines>=0 else '-' for l in self.cols])
        print '-' * indent + '+' + '-' * (2 * len(self.rows))
        for (s,g) in zip(labelLines,self.grid):
            print ' ' * (indent-len(s)) +  s + '|' + ' '.join('.' if c is None else 'X' if c else ' ' for c in g)
        print ""

    def isDone (self): # Does not check it is OK
        for l in self.grid:
            if None in l:
                return False
        return True

    def transpose (self):
        self.cols,self.rows=self.rows,self.cols
        self.grid=[list(i) for i in zip(*self.grid)]
        self.colFuel,self.rowFuel=self.rowFuel,self.colFuel

    def solve(self, depthHypo = 0):
        iter=0
        while True:
            assert(len(self.rows) == len(self.grid) and len(self.rows) == len(self.colFuel))
            for row,line,fuel in zip(self.rows, self.grid, self.colFuel):
                if (not useFuelToKnowWhenChangeHasBeenDone or fuel) and (None in line):
                    solveLine(row, line, self.rowFuel)
            if useFuelToKnowWhenChangeHasBeenDone:
                if True not in self.rowFuel:
                    break
                for i,f in enumerate(self.colFuel):
                    self.colFuel[i] = False
            else:
                if (iter>1 and oldGrid==self.grid):
                    break
            self.transpose()
            if not useFuelToKnowWhenChangeHasBeenDone:
                oldGrid = deepcopy(self.grid)
            iter+=1
            self.__str__()
        if iter%2:
            self.transpose()
        self.solveMakingHypothesis(depthHypo)

    def solveMakingHypothesis(self,depthHypo):
        if not self.isDone() and (depthHypo<maxLevelOfHypothesis or maxLevelOfHypothesis==-1):
            # This is where we decide if we go for depth first
            for i in range(0,len(self.grid)):
                for j in range(0,len(self.grid[i])):
                    if not self.isDone() and self.grid[i][j] is None:
                        self.tryHypothesis(i,j,depthHypo)
                
    def tryHypothesis(self,i,j, depthHypo):
        assert(self.grid[i][j] is None)
        for value in [True, False]:
            print  ' '*depthHypo, "Trying to put ", value, " in ", i, j
            tmp = deepcopy(self)
            tmp.grid[i][j] = value
            tmp.fuel[i][j] = True
            try:
                tmp.solve(depthHypo+1)
                if tmp.isDone():
                    print ' '*depthHypo, "Potential solution found - is it unique?"
            except Exception as e:
                print  ' '*depthHypo, "Caught exc: ", i, j, " must be ", not value
                self.grid[i][j] = not value
                self.fuel[i][j] = True
                self.solve(depthHypo)
                return
        print  ' '*depthHypo, "Trying ", i, j, " did not lead to anything"
       
@profile
def solveLine(values,line, fuel):
    print values
    if preventGenerationOfUselessCombinations and values and (False not in line) and (True not in line):
        assert(len(line)==len(fuel))
        lComb, rComb = getExtremeCombinations(values, len(line))
        for i,(left,right) in enumerate(zip(lComb, rComb)):
            if left and left==right:
                line[i], fuel[i] = True, True
    else:
        matchingComb = generateMatchingComb(values, line)
        if not matchingComb:
            raise Exception("No solution for ", values, line)
        first=matchingComb.pop()
        for i,c in enumerate(line):
            if c is None:
                r=first[i]
                for comb in matchingComb:
                     if comb[i]!=r:
                         r=None
                         break
                if r is not None:
                    line[i], fuel[i] = r, True

@timecall
def unitTest():
    for p in Picross.easyProblems():
        p.solve()
        assert(p.isDone())
    for p in Picross.hardProblems():
        p.solve()
        assert(not p.isDone())
    for p in Picross.easyProblems():
        p.transpose()
        p.solve()
        assert(p.isDone())
    for p in Picross.hardProblems():
        p.transpose()
        p.solve()
        assert(not p.isDone())

def perfTest():
    global useFuelToKnowWhenChangeHasBeenDone
    global stopGenerationAsSoonAsPossible
    global preventGenerationOfUselessCombinations
    booleans = [False, True]
    for useFuelToKnowWhenChangeHasBeenDone in booleans:
        for stopGenerationAsSoonAsPossible in booleans:
            for preventGenerationOfUselessCombinations in booleans:
                print "FUEL:",useFuelToKnowWhenChangeHasBeenDone, "STOP-GEN:", stopGenerationAsSoonAsPossible, "PREV-GEN:", preventGenerationOfUselessCombinations
                unitTest()
#perfTest()


def smallTest():
    p = Picross.problem17()
    p.__str__()
    p.solve()
    assert(p.isDone())
smallTest()
