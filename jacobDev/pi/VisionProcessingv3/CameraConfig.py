import logging

class visionConfig:
  import json

  def __init__(self, configFile = "visionConfig.json"):
    self.configFile = configFile
    self.teamID
    self.ntmode
    self.numCameras
    self.CameraConfigs


  def loadConfig(self, myCameraID):
    try:
        with open(self.configFile, "rt") as configFileHandle:
          j = json.load(configFileHandle)
    except OSError as err:
      logging.error('visionConfig.loadConfig(): %s failed to load using json.load(%s)', self.configFile, self.configFile)
      return False

    # Check that loaded json object is a dictionary
    if not isinstance(j, dict):
      logging.error('visionConfig.loadConfig(): %s is not in a JSON/"python dict" format.', self.configFile)
      return False

    try:
      self.teamID = j["teamID"]
    except KeyError:
      logging.warning('visionConfig.loadConfig(): unable to set teamID. Check if team element exists in %s', self.configFile)
      return False

    try:
      self.ntmode = j["ntmode"]
    except KeyError:
      logging.warning('visionConfig.loadConfig(): unable to set ntmode. Check if ntmode element exists in %s', self.configFile)
      return False

    try:
      self.ntid = j["ntid"]
    except KeyError:
      logging.warning('visionConfig.loadConfig(): unable to set ntid. Check if ntid element exists in %s', self.configFile)
      return False

    try:
      cameraConfigs = j["cameraConfigs"]
      numCameras = len(j[cameraConfigs])
    except KeyError:
      logging.warning('visionConfig.loadConfig(): unable to set cameraConfigs. Check if cameraConfigs element exists in %s', self.configFile)
      return False

    for i in range(0, numCameras):
      if cameraConfigs[i]["cameraID"] == myCameraID:
        self.cameraConfig = cameraConfigs[i]
      else
        logging.warning('visionConfig.loadConfig(): unable to set cameraConfig for %s. Check if cameraConfig element with cameraID %s exists in %s', myCameraID, myCameraID, self.configFile)
        return False

  return True










