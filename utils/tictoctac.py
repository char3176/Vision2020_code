import time
import logging

class tictoctac:

  def __init__(self, logging_verbosity = 1):
    self.instanceID = hex(id(self))
    self.instantiation_time = time.perf_counter()
    self.tic = None
    self.toc = None
    self.tac = None
    self.tac_ms = None

    # IGNORE THIS FOR NOW.  CHAR IMPLEMENTING Q&D LOGGER SO TIMINGS CAN BE RECORDED
    # TO LOG FILE FOR WHEN PI HAS NO VIDEO OUTPUT AVAILABLE
    logging.basicConfig(filename='tictoctac.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    if logging_verbosity == 1:
      logging.basicConfig(level=logging.DEBUG)
    elif logging_verbosity == 2:
      logging.basicConfig(level=logging.INFO)
    elif logging_verbosity == 3:
      logging.basicConfig(level=logging.WARNING)
    elif logging_verbosity == 4:
      logging.basicConfig(level=logging.ERROR)
    elif logging_verbosity == 5:
      logging.basicConfig(level=logging.CRITICAL)


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

  def setRawTac(self, x):
    self.tac = x

  def getRawTac(self):
    return self.tac

  def setTac_ms(self, x):
    self.tac_ms = x

  def getTac(self):
    return self.tac_ms

  def printTac(self):
    print("Benchmark Timing for object instance", self.instanceID, "(in milliseconds): ", self.tac_ms)
  def printRawTac(self):
    print("Benchmark Timing for object instance", self.instanceID, "(in fractional seconds): ", self.tac)




