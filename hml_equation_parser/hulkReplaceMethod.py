from typing import Dict, Tuple
import json, codecs
import os


with codecs.open(os.path.join(os.path.dirname(__file__),
                              "convertMap.json"),
                 "r", "utf8") as f:
    convertMap = json.load(f)

barDict = convertMap["BarConvertMap"]
matDict = convertMap["MatrixConvertMap"]
braceDict = convertMap["BraceConvertMap"]

def _findOutterBrackets(eqString: str, startIdx: int) -> Tuple[int, int]:
    '''
    eqString : equation string for converting.
    startIdx : the cursor of equation string to find brackets.
    return:
        (startCursor, endCursor) for outter brackets.
    '''
    idx = startIdx
    while True:
        idx -= 1
        if eqString[idx] == '{':
            break

    return _findBrackets(eqString, idx, direction=1)

def _findBrackets(eqString: str, startIdx: int, direction: int) -> Tuple[int, int]:
    '''
    eqString : equation string for converting.
    startIdx : the cursor of equation string to find brackets.
    direction : the direction of find.
        if 0, find brackets before the cursor.
           1, find brackets after the cursor.
    return:
        (startCursor, endCursor) for brackets.
    '''
    if direction == 1:
        startCur = eqString.find(r'{', startIdx)
        bracketCount = 1
        for i in range(startCur+1, len(eqString)):
            if eqString[i] == r'{':
                bracketCount += 1
            elif eqString[i] == r'}':
                bracketCount -= 1

            if bracketCount == 0:
                return (startCur, i+1)
    else:
        # reverse string and convert brackets.
        eqString = eqString[::-1]
        for idx, char in enumerate(eqString):
            if char == r'{':
                eqString = eqString[0:idx] + r'}' + eqString[idx+1:]
            if char == r'}':
                eqString = eqString[0:idx] + r'{' + eqString[idx+1:]

        # find brackets with new cursor
        newStartIdx = len(eqString) - (startIdx+1)
        startCur, endCur = _findBrackets(eqString, 
                                         newStartIdx,
                                         direction=1)
        return (len(eqString)- endCur,
                len(eqString)- startCur)
        
    raise ValueError("cannot find bracket")


def replaceAllBar(eqString: str) -> str:
    '''
    replace hat-like equation string.
    '''
    def replaceBar(eqString: str, barStr: str, barElem: str) -> str:
        cursor = 0

        while True:
            cursor = eqString.find(barStr)
            if cursor == -1:
                break
            try:
                eStart, eEnd = _findBrackets(eqString, cursor, direction=1)
                bStart, bEnd = _findOutterBrackets(eqString, cursor)
                elem = eqString[eStart:eEnd]
                
                beforeBar = eqString[0:bStart]
                afterBar = eqString[bEnd:]

                eqString = beforeBar + barElem + elem + afterBar
            except ValueError:
                return eqString
        return eqString

    for barKey, barElem in barDict.items():
        eqString = replaceBar(eqString, barKey, barElem)
    return eqString


def replaceAllMatrix(eqString: str) -> str:
    '''
    replace matrix-like equation
    '''
    def replaceElementsOfMatrix(bracketStr: str) -> str:
        '''
        replace the elements of matrix
        '''
        bracketStr = bracketStr[1:-1]  ## remove brackets
        
        bracketStr = bracketStr.replace(r'#',r' \\ ')
        bracketStr = bracketStr.replace(r'&amp;',r'&')

        return bracketStr

    def replaceMatrix(eqString: str, matStr: str, matElem: Dict[str, object]) -> str:
        cursor = 0
        while True:
            cursor = eqString.find(matStr)
            if cursor == -1:
                break
            try:
                eStart, eEnd = _findBrackets(eqString, cursor, direction=1)
                elem = replaceElementsOfMatrix(eqString[eStart:eEnd])

                if matElem['removeOutterBrackets'] == True:
                    bStart, bEnd = _findOutterBrackets(eqString, cursor)
                    beforeMat = eqString[0:bStart]
                    afterMat = eqString[bEnd:]
                else:
                    beforeMat = eqString[0:cursor]
                    afterMat = eqString[eEnd:]

                eqString = beforeMat + matElem['begin'] + \
                           elem + matElem['end'] + afterMat
            except ValueError:
                return eqString
        return eqString
    
    for matKey, matElem in matDict.items():
        eqString = replaceMatrix(eqString, matKey, matElem)
    return eqString


def replaceRootOf(eqString: str) -> str:
    '''
    `root {1} of {2}` -> `\sqrt[1]{2}`
    '''
    rootStr = r"root"
    ofStr = r"of"

    while True:
        rootCursor = eqString.find(rootStr)
        if rootCursor == -1:
            break
        try:
            ofCursor = eqString.find(ofStr)
            
            elem1 = _findBrackets(eqString, rootCursor, direction=1)
            elem2 = _findBrackets(eqString, ofCursor, direction=1)

            e1 = eqString[elem1[0]+1:elem1[1]-1]
            e2 = eqString[elem2[0]+1:elem2[1]-1]

            eqString = eqString[0:rootCursor] + \
                           r"\sqrt" + \
                           r"[" + e1 + r"]" +\
                           r"{" + e2 + r"}" +\
                           eqString[elem2[1]+1:]
        except ValueError:
            return eqString
    return eqString


def replaceFrac(eqString: str) -> str:
    '''
    `{1} over {2}` -> `\frac{1}{2}`
    '''
    hmlFracString = r"over"
    latexFracString = r"\frac"

    while True:
        cursor = eqString.find(hmlFracString)

        if cursor == -1:
            break
        try:
            # find numerator
            numStart, numEnd = _findBrackets(eqString, cursor, direction=0)
            numerator = eqString[numStart:numEnd]

            beforeFrac = eqString[0:numStart]
            afterFrac = eqString[cursor+len(hmlFracString):]

            eqString = beforeFrac + latexFracString + numerator + afterFrac
        except ValueError:
            return eqString
    return eqString



def replaceAllBrace(eqString: str) -> str:
    '''
    replace (over, under)brace equation string.
    '''
    def replaceBrace(eqString: str, braceStr: str, braceElem: str) -> str:
        cursor = 0

        while True:
            cursor = eqString.find(braceStr)
            if cursor == -1:
                break
            try:
                eStart1, eEnd1 = _findBrackets(eqString, cursor, direction=1)
                eStart2, eEnd2 = _findBrackets(eqString, eEnd1, direction=1)
                elem1 = eqString[eStart1:eEnd1]
                elem2 = eqString[eStart2:eEnd2]
                
                beforeBrace = eqString[0:cursor]
                afterBrace = eqString[eEnd2:]

                eqString = beforeBrace + braceElem + elem1 + '^' + elem2 + afterBrace
            except ValueError:
                return eqString
        return eqString

    for braceKey, braceElem in braceDict.items():
        eqString = replaceBrace(eqString, braceKey, braceElem)
    return eqString
