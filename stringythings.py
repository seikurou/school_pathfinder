import numpy as np
import math
class StringStuffs:
  @staticmethod
  def getColString(l, nCols, padding, allowOverflow=True):
    rString = ""
    startPos = np.empty(nCols)
    itemsPerCol = int(math.ceil(len(l)/float(nCols)))
    for i in range(len(startPos)):
      startPos[i] = i * itemsPerCol
    for i in range(itemsPerCol):
      for n in range(nCols):
        if startPos[n] >= len(l):
          rString += StringStuffs.padLeft("", padding, allowOverflow)
        else:
          rString += StringStuffs.padLeft(str(l[int(startPos[n])]), padding, allowOverflow)
        startPos[n] += 1
      rString += "\n"
    return rString
  @staticmethod
  def padLeft(string, pad, allowOverflow=True):
    if len(string) >= pad:
      if(allowOverflow):
        return string
      else:
        return string[:pad]
    for i in range(pad-len(string)):
      string += " "
    return string
