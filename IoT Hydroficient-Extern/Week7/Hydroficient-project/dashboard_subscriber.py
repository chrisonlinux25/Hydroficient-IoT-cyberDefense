import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime, timezone
import ssl   # ADD THIS FOR TLS


def on_connect(client, userdata, flags, reason_code, properties):
        print("\n" + "=" * 60)
        print("  GRAND MARINA WATER MONITORING DASHBOARD")
        print("  Connected at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 60)
        client.subscribe("hydroficient/grandmarina/#")

def on_message(client, userdata, msg):
    topic = msg.topic

    if "/sensors/" in topic:
        handle_sensor_reading(msg)
    elif "/alerts/" in topic:
        handle_alert(msg)
    elif "/commands/" in topic:
        handle_command(msg)
    elif "/status/" in topic:
        handle_status(msg)
    else:
        print(f"Unknown topic: {topic}")


def handle_sensor_reading(msg):
    try:
        data = json.loads(msg.payload.decode())
        display_reading(data)  # Uses your existing display_reading() function
    except json.JSONDecodeError:
        print(f"\n[RAW SENSOR MESSAGE] {msg.topic}")
        print(f"      {msg.payload.decode()}")

def handle_alert(msg):
    print(f"\n*** ALERT ***")
    print(f"Topic: {msg.topic}")
    print(f"Message: {msg.payload.decode()}")

def handle_command(msg):
    print(f"\n[COMMAND] {msg.topic}: {msg.payload.decode()}")

def handle_status(msg):
    # Could update a "last seen" tracker
    print(f"\n[STATUS] {msg.topic}: {msg.payload.decode()}")

def display_reading(data):
    """Format and display a sensor reading with alerts."""
    
    location = data.get('location', 'Unknown')
    device_id = data.get('device_id', 'Unknown')
    up = data.get('pressure_upstream', 0)
    down = data.get('pressure_downstream', 0)
    flow = data.get('flow_rate', 0)
    timestamp = data.get('timestamp', 'Unknown')
    counter = data.get('counter', 0)

 
    alerts = []

    if up > 90:
        alerts.append(
            "HIGH UPSTREAM PRESSURE"
        )

    if down < 65:
        alerts.append(
            "LOW DOWNSTREAM PRESSURE"
        )

    if flow > 60:
        alerts.append(
            "HIGH FLOW RATE - POSSIBLE LEAK"
        )

    if flow < 20:
        alerts.append(
            "LOW FLOW RATE - POSSIBLE BLOCKAGE"
        )
    # Display
    print(f"\n{'─' * 40}")
    print(f"  Location:  {location}")
    print(f"  Device ID: {device_id}")
    print(f"  Timestamp: {timestamp}")
    print(f"  Counter:   {counter}")

    if alerts:
        print(f"  *** ALERTS ***")
        for alert in alerts:
            print(f"  >>> {alert}")
    else:
     print("  Status: NORMAL")

    print(f"{'─' * 40}")
    print(f"  Pressure: {up:.1f} / {down:.1f} PSI")
    print(f"  Flow:     {flow:.1f} gal/min")
##

# Create and configure client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(
    ca_certs="certs/ca.pem",
    certfile=None,
    keyfile=None,
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS,
)
# Connect and run
print("Connecting to broker...")
client.connect("localhost", 8883)

print("Dashboard running. Press Ctrl+C to stop.")

client.loop_forever()