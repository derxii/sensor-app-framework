def get_debug_scan_devices():
    data = [
        ("Arduino HC-06", "M9SK1K31-252D-43E3-A986-DCF3CB63D08", -50) for _ in range(33)
    ]
    data += [("long device name", "NDKA92N-24124-1241", 9)]
    return data


def get_debug_sensor_names():
    data = {f"Sensor {i}" for i in range(16)}
    data.add("very long sensor name" * 2)
    return data
