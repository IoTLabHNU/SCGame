import json
from types import SimpleNamespace as Namespace


class ClientData:
  def __init__(self, roundNr, id, stock_fg, stock_ig, order, delivery):
    self.roundNr = roundNr
    self.id = id
    self.stock_fg = stock_fg
    self.order = order
    self.delivery = delivery
    self.stock_ig = stock_ig

  def __init__(self):
    self.roundNr = 0
    self.id = 0
    self.stock_fg = 0
    self.order = 0
    self.delivery = 0
    self.stock_ig = 0

  def obj2JSON(o):
    #print(o)
    s = json.dumps(o.__dict__) 
    return s
    
  @staticmethod  
  def json2obj(s):
    #print(s)
    c = json.loads(s, object_hook=lambda d: Namespace(**d))
    return c