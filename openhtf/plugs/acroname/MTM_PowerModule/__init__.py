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
Plugs that provide access to Acroname power module via USB/Ethernet.
For details of what these interfaces look like, see power_module_plug.py.


Note: 
	If this is the first time to use this plug or there is hardware change to BrainStem network, run the following cli script to set up the Brainstem network before use the plug:

	cli_scripts/acroname_power_module_on_brainstem_network_one_time_setup.py 

	The 3 variables, link_type, link_serial_number and power_module_serial_number need to match the real hardware that this plug interfaces with.
	
	link_type: (choose one from following:)
		USB 		(Host connecting to USB on power module directly)
		MTM_USBStem 	(Host connecting to power module through USBStem on MTM via USB)
		MTM_EtherStem	(Host connecting to power module through EtherStem on MTM via Ethernet)
	link_serial_number: 
		the serial number of link Stem (USBStem or EtherStem), ignore this if link_type==USB
	power_module_serial_number:
		the serial number of power module


Follow these steps to use the plug:

a. Configure BrainStem network parameters in .yaml file:
	MTM_PowerModule_Connection:
  		link_type: USB
  		router_address: 4
  		power_module_address: 6
  		link_serial_number: 0xCB6B1A04
  		power_module_serial_number: 0x2B8BFAE4
	MTM_PowerModule:
  		default_voltage_output: 4000000
  		default_current_limit: 1000000

b. Import this plug on top of test codes:

   from openhtf.plugs.acroname.MTM_PowerModule import power_module_plug

c.  Add the Python decorators on top of the test phases that will use the power module plug.

	@plug(power_module=power_module_plug.PowerSupplyControl)
	def test_phase(test,power_module):

c.  The right sequence to control power module:
	1. power_module.DiscoverAndConnectModule()

	2. power_module.ConfigurePowerSupply()
  	
	3. Check no short circuit beforeturn on
 		if power_module.NoShortCircuit():
    			print('Turn on power module...')
    			power_module.TurnOnPowerSupply()

	Optionally, measure voltage and current:
   		power_module.GetVoltage()
    		power_module.GetCurrent()
	Optionally, you can change voltage and current limit:
    		power_module.Set_Voltage_and_CurrentLimit(3300000,2000000)

"""
