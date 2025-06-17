import simpy
import random
import numpy as np
import pandas as pd
import sys

# Constants
ARRIVAL_MEAN = 5
WS1_SERVICE_MEAN = 6
WS2_SERVICE_MEAN = 8
WARMUP_TIME = 20  # minutes

class Stats:
    def __init__(self):
        self.time_in_system = []
        self.queue_times = []

def source(env, ws1, ws2, x, y, stats, ws2_active, run_until):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / ARRIVAL_MEAN))
        if env.now >= run_until:
            break
        env.process(entity(env, f"Entity_{i}", ws1, ws2, x, y, stats, ws2_active))
        i += 1

def entity(env, name, ws1, ws2, x, y, stats, ws2_active):
    arrival_time = env.now

    # Toggle WS2
    if len(ws1.queue) >= x:
        ws2_active[0] = True
    elif len(ws1.queue) < y:
        ws2_active[0] = False

    chosen_ws = random.choice([ws1, ws2]) if ws2_active[0] else ws1

    with chosen_ws.request() as req:
        queue_start = env.now
        yield req
        queue_time = env.now - queue_start

        service_time = random.expovariate(1.0 / (WS2_SERVICE_MEAN if chosen_ws == ws2 else WS1_SERVICE_MEAN))
        yield env.timeout(service_time)

    if arrival_time >= WARMUP_TIME:
        stats.time_in_system.append(env.now - arrival_time)
        stats.queue_times.append(queue_time)

def run_simulation(x, y, sim_time):
    total_time = WARMUP_TIME + sim_time
    ws2_active = [False]
    stats = Stats()
    env = simpy.Environment()
    ws1 = simpy.Resource(env, capacity=1)
    ws2 = simpy.Resource(env, capacity=1)

    env.process(source(env, ws1, ws2, x, y, stats, ws2_active, run_until=total_time))
    env.run(until=total_time)
    return stats

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 simulation.py <x> <y> <simulation_time>")
        sys.exit(1)

    x = int(sys.argv[1])
    y = int(sys.argv[2])
    sim_time = int(sys.argv[3])

    results = run_simulation(x, y, sim_time)

    print(f"\nSimulation Results (x={x}, y={y}, sim_time={sim_time} mins)")
    print("Average Time in System:", np.mean(results.time_in_system))
    print("Min Time in System:", np.min(results.time_in_system))
    print("Max Time in System:", np.max(results.time_in_system))
    print("Average Queue Time:", np.mean(results.queue_times))
    print("Total Entities Processed (after warm-up):", len(results.time_in_system))
