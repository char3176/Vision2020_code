import time

class tictoctac:

  def __init__(self):
    self.instanceID = hex(id(self))
    self.instantiation_time = time.perf_counter()
    self.tic = None
    self.toc = None
    self.tac = None
    self.tac_ms = None

  def markTic(self):
    self.tic = time.perf_counter()

  def setTic(self, x):
    self.tic = x

  def getTic(self):
    return self.tic

  def markToc(self):
    self.toc = time.perf_counter()
    self.calcTac()

  def setToc(self, x):
    self.toc = x
    self.calcTac()

  def getToc(self):
    return self.toc

  def calcTac(self):
    self.tac = self.toc - self.tic
    self.tac_ms = self.tac * 1000

  def setTac(self, x):
    self.tac = x

  def getTac(self):
    return self.tac

  def setTac_ms(self, x):
    self.tac_ms = x

  def getTac_ms(self, x):
    return self.tac_ms

  def printTac(self):
    print("Benchmark Timing for object instance", self.instanceID, "(in milliseconds): ", self.tac_ms)
  def printRawTac(self):
    print("Benchmark Timing for object instance", self.instanceID, "(in fractional seconds): ", self.tac)




