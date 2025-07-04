import torch
import time
import numpy as np
import threading

def stress_gpu(device: torch.device, seconds: int = 10):
    print(f"▶️ Starting GPU load for {seconds} seconds on {device}")
    size = 4096
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)
    start = time.time()
    iterations = 0
    while time.time() - start < seconds:
        c = torch.matmul(a, b)
        d = torch.relu(c)
        _ = torch.sum(d)
        if device.type == "cuda":
            torch.cuda.synchronize()
        iterations += 1
    print(f"✅ GPU stress finished. {iterations} iterations ran.\n")

def stress_cpu(seconds: int = 10):
    print(f"▶️ Starting CPU load for {seconds} seconds")
    size = 4096
    start = time.time()
    iterations = 0
    while time.time() - start < seconds:
        a = np.random.randn(size, size)
        b = np.random.randn(size, size)
        c = np.dot(a, b)
        d = np.maximum(c, 0)
        _ = np.sum(d)
        iterations += 1
    print(f"✅ CPU stress finished. {iterations} iterations ran.\n")

def stress_ram(gigabytes: int = 2, seconds: int = 10):
    print(f"▶️ Starting RAM load ~{gigabytes}GB for {seconds} seconds")
    blocks = []
    block_size = gigabytes * 256 
    start = time.time()
    while time.time() - start < seconds:
        blocks.append(np.zeros((block_size * 1024 * 1024 // 8,), dtype=np.float64))
        time.sleep(0.1)
    del blocks
    print("✅ RAM stress finished\n")

def stress_all(seconds: int = 10, ram_gb: int = 2):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    threads = [
        threading.Thread(target=stress_cpu, args=(seconds,)),
        threading.Thread(target=stress_gpu, args=(device, seconds)),
        threading.Thread(target=stress_ram, kwargs={"gigabytes": ram_gb, "seconds": seconds}),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("✅ Combined CPU + GPU + RAM stress finished\n")

if __name__ == "__main__":
    stress_all(seconds=15, ram_gb=2)
