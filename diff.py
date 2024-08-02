from pyats.topology import loader
from genie.conf import Genie
from genie.utils.diff import Diff
from datetime import datetime
import sys


# Load the testbed file
testbed = loader.load('testbed.yaml')

# Initialize Genie
genie_testbed = Genie.init(testbed)

# Get the list of device names from the testbed
device_names = list(genie_testbed.devices.keys())

if len(device_names) < 2:
    raise ValueError("The testbed must contain at least two devices for comparison.")

# Connect to the devices in sys.argv (user provided), or the first 2 if not provided.
if len(sys.argv) == 3:
    device1_name = sys.argv[1]
    device2_name = sys.argv[2]
else:
    device1_name = device_names[0]
    device2_name = device_names[1]

# Ensure the specified devices exist in the testbed
if device1_name not in genie_testbed.devices or device2_name not in genie_testbed.devices:
    raise ValueError("Specified devices not found in the testbed.")

device1 = genie_testbed.devices[device1_name]
device2 = genie_testbed.devices[device2_name]

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
filename = f"config_diff_{device1_name}_vs_{device2_name}_{timestamp}.txt"

# Save the diff to a file
with open(filename, 'w') as f:
    f.write(f"Configuration Difference between {device1_name} and {device2_name}\n")
    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(str(diff))

print(f"Diff output has been saved to {filename}")

# Disconnect from devices
device1.disconnect()
device2.disconnect()
