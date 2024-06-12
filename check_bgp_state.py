#!/usr/bin/python3
import subprocess
import sys

# Define the file path to read data from
file_path = 'output-exabgp'

try:
    # Use the 'cat' command to read the file and capture its output
    cat_process = subprocess.Popen(['cat', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    cat_output, cat_error = cat_process.communicate()

    if cat_process.returncode == 0:
        # Split the cat output into lines
        lines = cat_output.split('\n')

        # The first line contains headers, so we skip it
        data_lines = lines[1:]

        # Initialize variables to keep track of minimum uptime and total uptime
        min_uptime_minutes = float('inf')
        total_uptime_minutes = 0

        # Count the number of established BGP sessions and calculate total uptime in minutes
        num_sessions = len(data_lines)

        for line in data_lines:
            fields = line.split()
            if len(fields) >= 3:
                uptime_minutes = int(fields[2]) * 24 * 60
                total_uptime_minutes += uptime_minutes
                if uptime_minutes < min_uptime_minutes:
                    min_uptime_minutes = uptime_minutes

        # Determine the smallest time period (either "days" or "hours") for uptime
        if min_uptime_minutes >= (24 * 60):
            min_uptime = "{} days".format(min_uptime_minutes // (24 * 60))
        else:
            min_uptime = "{} hours".format(min_uptime_minutes // 60)

        if num_sessions == 2:
            status = "OK"
            print(f"OK - BGP sessions look ok, found {num_sessions} sessions")
        else:
            status = "WARNING"
            print(f"WARNING - found less or more than 2 BGP session, found {num_sessions}")
        
        # Print the session details
        for line in data_lines:
            print(f"{min_uptime} {line}")
        
        # Exit with a specific code
        sys.exit(0 if status == "OK" else 1)
        
    else:
        print(f"Error running 'cat': {cat_error}")
        sys.exit(1)

# Handle other exceptions
except Exception as e:
    print(f"An error occurred: {str(e)}")
    sys.exit(1)
