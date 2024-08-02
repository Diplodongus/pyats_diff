from pyats.topology import loader
from genie.conf import Genie
from genie.utils.diff import Diff

# Load the testbed file
testbed = loader.load('testbed.yaml')

# Initialize Genie
genie_testbed = Genie.init(testbed)

# Connect to devices
device1 = genie_testbed.devices['device1']
device2 = genie_testbed.devices['device2']

device1.connect()
device2.connect()

# Learn the entire config for both devices
device1_config = device1.learn('config')
device2_config = device2.learn('config')

# Perform the diff
diff = Diff(device1_config, device2_config)
diff.findDiff()

# Print the diff
print(diff)

# Disconnect from devices
device1.disconnect()
device2.disconnect()
