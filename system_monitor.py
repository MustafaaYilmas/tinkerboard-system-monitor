import csv
import subprocess
import time

# Retrieve CPU usage for all cores
def get_cpu_usage():
    # Command to fetch the CPU utilization details
    cmd = "mpstat -P ALL 1 1 | awk '/Average:/ && $2 ~ /[0-9]/ {print $3}'"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split("\n")
    return [float(usage) for usage in result]

# Retrieve RAM and Swap memory usage details
def get_ram_swap_usage():
    # Command to fetch the RAM and Swap memory utilization
    cmd = "free -m | awk 'NR==2{print $3,$4} NR==3{print $3,$4}'"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split("\n")
    ram_used, ram_free, swap_used, swap_free = map(int, ' '.join(result).split())
    return ram_used, ram_free, swap_used, swap_free

# Retrieve disk usage details for root partition
def get_disk_usage():
    # Command to fetch the disk utilization of root directory
    cmd = "df -h / | awk 'NR==2{print $3,$4}'"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split()
    used, available = result
    return used, available

# Get the system temperature
def get_temperature():
    try:
        # Read temperature from system file
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as temp_file:
            temperature = int(temp_file.read()) / 1000  # Convert milicelsius value to celsius
        return f"{temperature}°C"
    except:
        return "N/A"

# Retrieve disk I/O details
def get_disk_io():
    # Command to fetch the disk read/write speed
    cmd = "iostat -d -y 1 1 | awk 'NR==4 {print $3,$4}'"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip().split()
    read_speed, write_speed = result
    return read_speed, write_speed

# Get the network usage details for a specific interface
def get_network_usage(interface="wlan0"):
    # Initialize variables to hold current values
    current_received, current_sent = 0, 0
    
    # Initialize variables to hold previous values (initially set to 0)
    prev_received, prev_sent = 0, 0

    with open("/proc/net/dev", "r") as f:
        lines = f.readlines()

    # Find the line containing data for the desired interface
    for line in lines:
        if interface in line:
            data = line.split()
            current_received = int(data[1]) / 1024
            current_sent = int(data[9]) / 1024
            break

    # Calculate the instantaneous usage
    recv_rate = current_received - prev_received
    sent_rate = current_sent - prev_sent

    # Store the current values for the next iteration
    prev_received, prev_sent = current_received, current_sent

    # Return both instantaneous and cumulative values
    return recv_rate, sent_rate, current_received, current_sent

# Open a CSV file and write system metrics to it every second
with open('system_metrics.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "CPU1", "CPU2", "CPU3", "CPU4", "RAM_Used", "RAM_Free", "Swap_Used", "Swap_Free", "Disk_Used", "Disk_Available", "Disk_Read_Speed", "Disk_Write_Speed", "Net_Received_Rate", "Net_Sent_Rate", "Total_Net_Received", "Total_Net_Sent", "Temperature"])
    
    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        cpu_usages = get_cpu_usage()
        ram_used, ram_free, swap_used, swap_free = get_ram_swap_usage()
        disk_used, disk_available = get_disk_usage()
        disk_read_speed, disk_write_speed = get_disk_io()
        recv_rate, sent_rate, total_received, total_sent = get_network_usage()
        temperature = get_temperature()

        writer.writerow([current_time] + cpu_usages + [ram_used, ram_free, swap_used, swap_free, disk_used, disk_available, disk_read_speed, disk_write_speed, recv_rate, sent_rate, total_received, total_sent, temperature])
        time.sleep(1)
