# Copyright 2014 Google Inc. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Acroname power module plug for OpenHTF."""


import logging
import time
from time import sleep

import openhtf.conf as conf
import openhtf.plugs as plugs

from brainstem import discover
from brainstem.link import Spec
from brainstem.stem import MTMPM1
from brainstem.stem import MTMEtherStem
from brainstem.stem import MTMUSBStem
from brainstem.defs import model_info

# _LOG = logging.getLogger("openhtf.example.plugs.acroname.power_module_plug.py")
_LOG = logging.getLogger(__name__)

conf.Declare('MTM_PowerModule',
             description='MTM Power Module configurations voltage output in uV and current limit in uA.')

# conf.Declare('default_power_module_current_limit',
#             description='Defalut power module current limit in uA.')

conf.Declare('MTM_PowerModule_Connection',
             description='MTM Power Module COnnection Parameters.')




class PowerModuleError(Exception):
 """Error connecting or controlling Acroname power module."""



def CheckReturnCode(code, action_str):
  if not code:
    _LOG.info("Result of %s: %d", action_str, code)
  else:
    _LOG.error("""Error connecting or controlling power module while attempting to %s: %d""", action_str,code)
    raise PowerModuleError() 


class PowerSupplyControl(plugs.BasePlug):   # pylint: disable=no-init
  """Acronmae power module control plug."""
  

  def __init__(self):
    config = conf.Config()
    self.connection_type = config.MTM_PowerModule_Connection['link_type']
    self.link_module_serial_number = config.MTM_PowerModule_Connection['link_serial_number']
    self.power_module_serial_number = config.MTM_PowerModule_Connection['power_module_serial_number']
    self.voltage = config.MTM_PowerModule['default_voltage_output']
    self.current_limit = config.MTM_PowerModule['default_current_limit']
    # self.is_first_time_setup = config.MTM_PowerModule_Connection['first_time_setup']
    self.MTMPowerModuleAddress = config.MTM_PowerModule_Connection['power_module_address']
    self.routerAddress = config.MTM_PowerModule_Connection['router_address'] 
    if self.connection_type == 'MTM_EtherStem':
      self.link_stem = MTMEtherStem()
    elif self.connection_type == 'MTM_USBStem': 
      self.link_stem = MTMUSBStem()

    self.power_module = MTMPM1()
    
  def DiscoverAndConnectModule(self):
    """
    Discover a power module if it is not connected yet.
    Connect the one with the serial number specified in config yaml file.
    """
    # spec = discover.find_first_module(Spec.TCPIP)
    # print "Is power module connected?"
    # print self.power_module.is_connected()

    if self.connection_type == 'USB':
      # spec = discover.find_all(Spec.USB)
      #spec = discover.find_module(Spec.USB,self.power_module_serial_number)
      # print "spec: "+str(spec)
      # print "USB serial number: 0x" + str(hex(spec[0].serial_number))
      res = self.power_module.connect(self.power_module_serial_number)
      # print "power module connection res: %d"%res
      """
      if self.is_first_time_setup:
        res = self.power_module.system.setRouter(self.MTMPowerModuleAddress)
        #CheckReturnCode(res, "setRouterAddress")
      
        res = self.power_module.system.save()
        #CheckReturnCode(res, "LinkStemSave")

        res = self.power_module.system.reset()
        #CheckReturnCode(res, "PowerModulereset")
        sleep(0.1)
      """
      # print("is power module connected? %d"%self.power_module.is_connected())
      #CheckReturnCode(res, "power_module.connect")
      _LOG.info("Connected to Power Module with serial number: ",hex(self.power_module_serial_number).upper())
      
    else:
      # print "Connecting to link stem..."
      
      res = self.link_stem.connect(self.link_module_serial_number)
      #CheckReturnCode(res, "link_stem.connect")
      _LOG.info("Connected to Link Module with serial number: ",hex(self.link_module_serial_number).upper())
      # print "Is link stem connected now?"
      # print self.link_stem.is_connected()

      res = self.power_module.connect_through_link_module(self.link_stem)
      # print "Is power module connected now?"
      # print self.power_module.is_connected() 
      """
      if self.is_first_time_setup:
        # This is one-time configuration to set up the network
        res = self.link_stem.i2c[0].setPullup(1)
        #CheckReturnCode(res, "LinkStemsetPullUp")

        # set link stem object to talk to the power module 
        # res = self.link_stem.setModuleAddress(self.MTMPowerModuleAddress)
        # CheckReturnCode(res, "setModuleAddress")

        # get the module address the link_stem's link is connected to
        # we will set this as the BrainStem network router
        
        #res = self.link_stem.module()
        #routerAddress = res

        # set the link stem's module address offsets to 0
        # we will assume the link stem hardware offsets are 0
        res = self.link_stem.system.setModuleSoftwareOffset(0)

        # set the link stem's router address
        res = self.link_stem.system.setRouter(self.routerAddress)
        #CheckReturnCode(res, "setRouterAddress")
      
        res = self.power_module.system.setRouter(self.routerAddress)
        #CheckReturnCode(res, "setRouterAddress")

        res = self.link_stem.system.save()
        #CheckReturnCode(res, "LinkStemSave")

        res = self.power_module.system.save()
        #CheckReturnCode(res, "PowerModuleSave")
    
        res = self.power_module.system.reset()
        #CheckReturnCode(res, "PowerModulereset")
    
        res = self.link_stem.system.reset()
        #CheckReturnCode(res, "Linkreset")
        sleep(0.1)
      """
      # print "Is power module connected now?"
      # print self.power_module.is_connected() 
      # res = self.power_module.connect_through_link_module(self.EtherStem)
      # CheckReturnCode(res, "PowerModuleConnectThroughLink")
      # res = self.link_stem.connect(self.link_module_serial_number)
      # CheckReturnCode(res, "PowerModuleConnectThroughLink")
      # res = self.power_module.connect_through_link_module(self.link_stem)
      # CheckReturnCode(res, "PowerModuleConnectThroughLink")

  def NoShortCircuit(self):
    """
    Check if there is short on Power Module by driving one GPIO high.
    And read GPIO state to ensure it is actually high.
    """
    self.power_module.digital[0].setConfiguration(1)
    self.power_module.digital[0].setState(1)
    digital0State = self.power_module.digital[0].getState()
    nAttempts = 3
    while (digital0State.value != 1) and nAttempts:
        digital0State = self.power_module.digital[0].getState()
        nAttempts = nAttempts -1
        #print "power_module digital0State: %d" %digital0State.value
        _LOG.info("power_module digital0State: "+str(digital0State.value))
    if digital0State.value != 1:
        _LOG.info("digital0State: "+str(digital0State.value))
        # print "digital0State: %d" %digital0State.value
        self.power_module.rail[0].setEnableExternal(0)
        self.power_module.digital[0].setState(0)
        _LOG.info("Power module is not in right state.There is short circuit. Close connection.")
        raise PowerModuleError
        # print "Power module is not in right state. Close connection."
        # return False
    else:
        # print "Power module is in right state. Continue."
        return True

  def ConfigurePowerSupply(self):  # pylint: disable=no-self-use
    """Set Voltage, Current Limit, operational mode, kelvin sensing mode..."""
    res = self.power_module.rail[0].setKelvinSensingMode(1)
    # CheckReturnCode(res,"setKelvinSensingMode")

    res = self.power_module.rail[0].setOperationalMode(1)
    #CheckReturnCode(res,"setOperationalMode")

    self.Set_Voltage_and_CurrentLimit(self.voltage,self.current_limit)
    # self.ChangeVoltage(self.voltage)
    # self.ChangeCurrentLimit(self.current_limit)
    

  def TurnOnPowerSupply(self):
    """"""
    res = self.power_module.rail[0].setEnableExternal(1)
    voltage_meas = self.GetVoltage()
    if res == 0 and ( 
      (self.voltage-0.5e6)<=voltage_meas<=(self.voltage+500000)):
        # print "Succeed in turning on power supply."
      _LOG.info("Succeed in turning on power supply.")
    else:
      # print "Error enabling rail0: res = "+str(res)
      # print "GetVoltage: %d"%voltage_meas
      # print "Error turning on power supply."
      _LOG.info("Error turning on power supply.")
      CheckReturnCode(res,"TurnOnPowerSupply")

  def GetVoltage(self):
    """Measure voltage and return voltage value."""
    for i in range(3):
      res = self.power_module.rail[0].getVoltage()
      vmeas=0.0
      if res.error == 0:
        vmeas = res.value
        break
      elif i ==2:
        # print "GetVoltage(): Error getting power module voltage: %d"%(res.error)
        #print "GetVoltage(): %.3f" % (res.value)
        CheckReturnCode(res.error,"GetVoltage")
        return 0.0
    # print ("vmeas = %d uV" %vmeas)
    # v = round((float(vmeas)/float(1000000)))
    return vmeas

  def GetCurrent(self):
    """Measure current and return current value."""
    imeas = self.power_module.rail[0].getCurrent().value
    error = self.power_module.rail[0].getCurrent().error
    # print("GetCurrent Error:%d"%error)
    # print("imeas=%d uA" %imeas)
    # i = float(imeas/1000000)
    return imeas

  def Set_Voltage_and_CurrentLimit(self, voltage_uV,current_limit_uA):
    """Set output voltage value and current limit."""
    # res1 = self.power_module.rail[0].setEnableExternal(0)
    # sleep(0.5)
    for i in range(3):
      res = self.power_module.rail[0].setVoltage(voltage_uV)
      # sleep(0.1)
      # vmeas_uV = self.GetVoltage()
      # print "change vmeas=: %d"%vmeas_uV
      if res==0:
      # if res==0 and (
      #   (voltage_uV-500000)<=vmeas_uV<=(voltage_uV+500000)):
        # res3 = self.power_module.rail[0].setEnableExternal(1)
        # if res3 ==0:
        # print "Succeed in changing voltage."
        _LOG.info("Succeed in changing voltage.")
        break
        #else:
        #  raise ChangeVoltageError
      elif i==2:
        # print "Error in changing voltage: res: %d" %res
        # print "vmeas_uV=: %d"%vmeas_uV
        _LOG.info("Error in changing voltage.")
        CheckReturnCode(res,"SetVoltageOuput")

    res = self.power_module.rail[0].setCurrentLimit(current_limit_uA)
    # print ("vmeas = %d uV" %vmeas)
    # v = round((float(vmeas)/float(1000000)))
    CheckReturnCode(res,"SetCurrentLimit")

  """
  def SetVoltage(self, voltage_uV):
    # Set output voltage value.
    # res1 = self.power_module.rail[0].setEnableExternal(0)
    # sleep(0.5)
    for i in range(3):
      res = self.power_module.rail[0].setVoltage(voltage_uV)
      #sleep(0.1)
      vmeas_uV = self.GetVoltage()
      # print "change vmeas=: %d"%vmeas_uV
      if res==0 and (
        (voltage_uV-500000)<=vmeas_uV<=(voltage_uV+500000)):
        # res3 = self.power_module.rail[0].setEnableExternal(1)
        # if res3 ==0:
        # print "Succeed in changing voltage."
        _LOG.info("Succeed in changing voltage.")
        break
        #else:
        #  raise ChangeVoltageError
      elif i==2:
        # print "Error in changing voltage: res: %d" %res
        # print "vmeas_uV=: %d"%vmeas_uV
        _LOG.info("Error in changing voltage.")
        raise PowerModuleError


  def SetCurrentLimit(self,current_limit_uA):
    # Set current limit value.
    # res1 = self.power_module.rail[0].setEnableExternal(0)
    # sleep(0.5)
    res = self.power_module.rail[0].setCurrentLimit(current_limit_uA)
    # print ("vmeas = %d uV" %vmeas)
    # v = round((float(vmeas)/float(1000000)))
    CheckReturnCode(res,"ChangeCurrentLimit")
  """

  def PowerOff(self):
    """"""
    for i in range(3):
      res = self.power_module.rail[0].setEnableExternal(0)
      if res == 0:
        # print "Succeed in turning off power supply."
        _LOG.info("Succeed in turning off power supply.")
        break
      elif i==2:
        # print "Error turning off power supply:"
        # print "res = %d" %res
        _LOG.info("Error turning of power supply.")
        CheckReturnCode(res,"PowerOff")
  
  def Disconnect(self):
    """"""
    self.power_module.disconnect()
    if self.connection_type != 'USB':
      self.link_stem.disconnect()
  
  
  def TearDown(self):
    """This method is optional.

    If implemented, it will be called at the end
    of the test.
    """
    self.Disconnect()