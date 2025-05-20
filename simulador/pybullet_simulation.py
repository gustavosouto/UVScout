import pybullet as p
import pybullet_data
import time
import paho.mqtt.client as mqtt
import json
import random

client = mqtt.Client()
client.connect("localhost", 1883)

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF("plane.urdf")
robot = p.loadURDF("r2d2.urdf", [0, 0, 0.1])

p.setGravity(0, 0, -9.8)

waypoints = [[2, 2], [3, -1], [0, -3], [-2, 1]]

for wp in waypoints:
    target_x, target_y = wp
    for _ in range(100):
        pos, _ = p.getBasePositionAndOrientation(robot)
        dx = target_x - pos[0]
        dy = target_y - pos[1]
        new_pos = [pos[0] + 0.01 * dx, pos[1] + 0.01 * dy, pos[2]]
        p.resetBasePositionAndOrientation(robot, new_pos, [0, 0, 0, 1])
        uv_reading = round(random.uniform(0.5, 8.0), 2)

        payload = {
            "id": "UVScout01",
            "x": new_pos[0],
            "y": new_pos[1],
            "uvIndex": uv_reading
        }

        client.publish("robot/uv", json.dumps(payload))
        time.sleep(0.1)

p.disconnect()
