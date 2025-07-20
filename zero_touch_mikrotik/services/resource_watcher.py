import psutil

def get_cpu_usage():
    """Returns the current CPU usage as a percentage."""
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    """Returns the current RAM usage as a percentage."""
    return psutil.virtual_memory().percent

def get_bandwidth_usage():
    """
    Returns the current bandwidth usage in Mbps.
    This is a placeholder and needs to be implemented based on the specific system and network interface.
    """
    # Placeholder: returning a fixed value
    # In a real implementation, you would use a library like `speedtest-cli` or monitor network interface stats.
    return 10.0

def is_system_idle(cpu_threshold=50, ram_threshold=80):
    """
    Checks if the system is idle based on CPU and RAM usage.
    """
    cpu_usage = get_cpu_usage()
    ram_usage = get_ram_usage()
    print(f"Current CPU usage: {cpu_usage}%")
    print(f"Current RAM usage: {ram_usage}%")
    return cpu_usage < cpu_threshold and ram_usage < ram_threshold
