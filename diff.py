from pyats.topology import loader
from genie.conf import Genie
from genie.utils.diff import Diff
from datetime import datetime

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

# Generate a filename with current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"config_diff_{device1.name}_vs_{device2.name}_{timestamp}.txt"

# Save the diff to a file
with open(filename, 'w') as f:
    f.write(f"Configuration Difference between {device1.name} and {device2.name}\n")
    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(str(diff))

print(f"Diff output has been saved to {filename}")

# Disconnect from devices
device1.disconnect()
device2.disconnect()
