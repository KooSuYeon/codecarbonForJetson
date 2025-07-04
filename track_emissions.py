from codecarbon import EmissionsTracker
from jtop import jtop
import time, threading, csv
from datetime import datetime

"""
This script uses the CodeCarbon library to automatically track CO₂ emissions from CPU and RAM usage.
GPU energy consumption and CO₂ emissions are measured and calculated separately using the jtop library.
- CodeCarbon: Estimates CO₂ emissions based on CPU and RAM usage.
- jtop: Measures GPU power consumption on Jetson boards and calculates energy and CO₂.

GPU CO₂ emissions are estimated by multiplying GPU energy (kWh) by the GPU_CO2_FACTOR.
Results are saved to 'gpu_log.csv' and 'total_summary.csv'.
"""


GPU_CO2_FACTOR = 0.5

class GPUEnergyMonitor(threading.Thread):
    def __init__(self, duration_sec=10, interval_sec=1, output_file="gpu_log.csv"):
        super().__init__()
        self.duration_sec = duration_sec
        self.interval_sec = interval_sec
        self.output_file = output_file
        self._stop_flag = False
        self.data = []
        self.total_energy_kwh = 0.0

    def run(self):
        with jtop() as jet:
            start_time = time.time()
            while not self._stop_flag and (time.time() - start_time) < self.duration_sec:
                stats = jet.stats
                power_w = float(stats.get("Power GPU", 0.0))
                ts = datetime.utcnow().isoformat()
                energy_kwh = power_w / 1000 / 3600
                co2_kg = energy_kwh * GPU_CO2_FACTOR
                self.total_energy_kwh += energy_kwh
                print(f"[{ts}] GPU Power: {power_w:.2f} W")
                self.data.append((ts, f"{power_w:.2f}", f"{energy_kwh:.8f}", f"{co2_kg:.8f}"))
                time.sleep(self.interval_sec)

    def stop(self):
        self._stop_flag = True

    def save_to_csv(self):
        with open(self.output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "gpu_power_w", "gpu_energy_kwh", "gpu_co2_kg"])
            writer.writerows(self.data)
        print(f"✅ GPU log saved → {self.output_file}")

def workload(duration_sec=10):
    tracker = EmissionsTracker()
    tracker.start()
    gpu_mon = GPUEnergyMonitor(duration_sec=duration_sec)
    gpu_mon.start()
    time.sleep(duration_sec)
    gpu_mon.stop()
    gpu_mon.join()
    gpu_mon.save_to_csv()
    gpu_energy = gpu_mon.total_energy_kwh

    emissions = tracker.stop()

    print(f"GPU energy consumed: {gpu_energy:.6f} kWh")
    print(f"Total CO₂ emissions (CPU+RAM): {emissions:.6f} kg")

    total_co2 = emissions + gpu_energy * GPU_CO2_FACTOR
    gpu_co2 = gpu_energy * GPU_CO2_FACTOR

    with open("total_summary.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["gpu_energy_kwh", "cpu_ram_co2_kg", "gpu_co2_kg", "total_co2_kg"])
        writer.writerow([gpu_energy, emissions, gpu_co2, total_co2])
    print("✅ Total summary saved to total_summary.csv")

    return gpu_energy


if __name__ == "__main__":
    gpu_energy = workload(10)
    gpu_co2 = gpu_energy * GPU_CO2_FACTOR
    print(f"🌿 Estimated GPU CO₂ emissions: {gpu_co2:.6f} kg")
    print("🔥 CPU and RAM CO₂ emissions are automatically tracked by CodeCarbon.")
