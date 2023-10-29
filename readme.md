## README.md

### System Metrics Collector

This script is designed to capture and record key system metrics at regular intervals. The data includes CPU usage, RAM and Swap memory details, disk usage, system temperature, disk I/O speeds, and network usage details. All this data is written to a CSV file named `system_metrics.csv` every second.

#### Metrics Captured:

- **CPU Usage**: Captures the CPU utilization percentage for all cores.
- **RAM and Swap Usage**: Retrieves the amount of used and free memory in megabytes.
- **Disk Usage**: Fetches the disk utilization (used and available space) for the root directory.
- **System Temperature**: Obtains the system temperature in Celsius.
- **Disk I/O**: Retrieves the read and write speeds of the disk.
- **Network Usage**: Captures the instantaneous network usage (received and sent rate) and cumulative network usage (total bytes received and sent) for a specified interface (default is "wlan0").

#### Prerequisites

Before running the script, make sure you have the following tools installed on your system:

- `mpstat` (part of the `sysstat` package): For retrieving CPU utilization details.
- `free`: For obtaining RAM and Swap memory usage details.
- `df`: For fetching disk utilization details.
- `iostat` (also part of the `sysstat` package): For capturing disk I/O details.
- Permissions to read system-specific files (like `/sys/class/thermal/thermal_zone0/temp` and `/proc/net/dev`).

#### How to Setup and Run

1. Ensure all the required packages and tools are installed.
2. Run the script.
3. Check the generated `system_metrics.csv` for the collected metrics.

You can use the provided `setup.sh` script to install the necessary packages.

#### setup.sh

```sh
#!/bin/bash

# Update the package list
sudo apt-get update

# Install sysstat package which provides mpstat and iostat commands
sudo apt-get install -y sysstat

# Note: Other commands like 'free' and 'df' are generally pre-installed on most Linux distributions.
```

Save the above content to a file named `setup.sh`, and give it execution permissions using the command:

```bash
chmod +x setup.sh
```

After that, you can run `./setup.sh` to install the necessary packages.

#### Note

The script assumes a system with four CPU cores. If your system has a different number of cores, you may need to adjust the CSV headers and related sections accordingly.

Also, always make sure to monitor the size of `system_metrics.csv` since the script keeps appending data every second. Depending on your use case, you might want to run the script for specific durations or implement a rotation mechanism for the CSV file.

---

I hope this README provides a comprehensive overview of the script and its functionalities. Let me know if you need any further details or clarifications!
