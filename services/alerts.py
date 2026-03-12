def check_latency(latency_seconds):
    if latency_seconds <= 180:
        return "Normal"
    elif latency_seconds <= 300:
        return "Warning"
    else:
        return "Critical"
