

def feet2inches(feet):
  return feet * 12

def inches2feet(inches):
  feet = inches / 12.0
  remainder_inches = feet % 12.0
  return feet, remainder_inches

def inches2meters(inches):
  return inches * 39.37007874

def meters2inches(meters):
  return meters / 0.0254

def meters2feet(meters):
  inches = meters2inches(meters)
  feet, remainder_inches = inches2feet(inches)
  return feet, remainder_inches


