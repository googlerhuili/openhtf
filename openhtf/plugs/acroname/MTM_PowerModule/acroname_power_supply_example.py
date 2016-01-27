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


"""
Example of Acronmae Power Module control logic.

Run with (your virtualenv must be activated first):
python ./acroname_power_supply_example.py --config ./acroname_power_supply_example.yaml

To log info into a file, add 2 flags following the command above:
--log_file <LogFileName> --log_level info
"""


import tempfile
import time
from time import sleep

#import example_plug
import openhtf 
from openhtf.plugs.acroname.MTM_PowerModule import power_module_plug

from openhtf.names import *



# @TestPhase(timeout_s= 3)
@plug(power_module=power_module_plug.PowerSupplyControl)
def discover_and_connect_power_module(test, power_module):
  #Test phase that discovers and connects power module.
  print('Connecting the BrainStem network...')
  #test.logger.info('Discover and connect power module...')
  # print('Trying to connect...')
  power_module.DiscoverAndConnectModule()
  #test.logger.info('Success in connect!')
  print('Success in connect!')





@plug(power_module=power_module_plug.PowerSupplyControl)
#@TestPhase(timeout_s=10)
def configure_and_turn_on_power_module(test, power_module):
  #Test phase that configures and turns on power module.
  test.logger.info('Checking and configuring power module...')
  print('Checking and configuring power module...')
  #if power_module.NoShortCircuit():
  power_module.ConfigurePowerSupply() 
    # set voltage and current limit to defalut values defined in .yaml file
    # default_power_module_voltage_output: 5000000
    # default_power_module_current_limit: 1000000
  power_module.TurnOnPowerSupply()

  #else:
    # short circuit error would be raised in the plug
  #  test.logger.info('Short circuit found on power module!')
  #  print('Short circuit found on power module!')
  #  raise PowerModuleShortCircuitError



# Timeout if this phase takes longer than 10 seconds.
#@TestPhase(timeout_s=10)
@measures([Measurement(
  'acroname_power_voltage').Number().InRange(4900000,5100000).Doc(
  'Voltage of Acroname Power Module Output, Unit: uV')])
@measures([Measurement(
  'acroname_power_current').Number().InRange(0,1000000).Doc(
  'Current of Acroname Power Module Output, Unit: uA')])
@plug(power_module=power_module_plug.PowerSupplyControl)
def get_power_module_measurements(test,power_module):
  """Test phase that gets acroname power measurement."""
  test.measurements.acroname_power_voltage = power_module.GetVoltage()
  print("voltage = %d uV" %test.measurements.acroname_power_voltage)
  test.measurements.acroname_power_current = power_module.GetCurrent()
  print("current = %d uA" %test.measurements.acroname_power_current)


# Timeout if this phase takes longer than 10 seconds.
#@TestPhase(timeout_s=10)
@plug(power_module=power_module_plug.PowerSupplyControl)
def power_module_change_voltage_current_limit(test,power_module):
  """Test phase that gets acroname power measurement."""
  power_module.ChangeVoltage(3300000)
  power_module.ChangeCurrentLimit(2000000)



# Timeout if this phase takes longer than 10 seconds.
#@TestPhase(timeout_s=10)
@measures([Measurement(
  'acroname_power_voltage2').Number().InRange(3200000,3400000).Doc(
  'Voltage of Acroname Power Module Output, Unit: uV')])
@measures([Measurement(
  'acroname_power_current2').Number().InRange(0,2000000).Doc(
  'Current of Acroname Power Module Output, Unit: uA')])
@plug(power_module=power_module_plug.PowerSupplyControl)
def get_power_module_measurements2(test,power_module):
  """Test phase that gets acroname power measurement."""
  test.measurements.acroname_power_voltage2 = power_module.GetVoltage()
  print("voltage2 = %d uV" %test.measurements.acroname_power_voltage2)
  test.measurements.acroname_power_current2 = power_module.GetCurrent()
  print("current2 = %d uA" %test.measurements.acroname_power_current2)



# Timeout if this phase takes longer than 10 seconds.
#@TestPhase(timeout_s=10)
@plug(power_module=power_module_plug.PowerSupplyControl)
def turn_off_and_disconnect_power_module(test,power_module):
  """Test phase that turns off and disconnects acroname power measurement."""
  power_module.PowerOff()
  power_module.Disconnect()





if __name__ == '__main__':
  test = openhtf.Test(discover_and_connect_power_module,
                       configure_and_turn_on_power_module,
                       get_power_module_measurements,
                       power_module_change_voltage_current_limit,
                       get_power_module_measurements2,
                       turn_off_and_disconnect_power_module)

  #cleanUp = openhtf.Test(turn_off_and_disconnect_power_module)
  #test.AddOutputCallback(OutputToJSON(
  #		'./%(dut_id)s.%(start_time_millis)s', indent=4))
  #test.Execute(test_start=triggers.PromptForTestStart())
  
  test.Execute()
  
  #cleanUp.Execute()