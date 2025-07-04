## Challenges

CodeCarbon tracks CPU and RAM energy consumption by default, and GPU-related features are not yet fully supported.
(Officially, you can set up metadata such as gpu_count and gpu_name related to GPU, but,The ability to accurately track CO₂ emissions by directly measuring or automatically recognizing GPU power usage is limited.)

→ 

### So I use `jtop` to collect GPU power data separately,
I measured the GPU's energy consumption by using this data combined with CodeCarbon CPU/RAM emissions

> *GPU Energy Info From Jtop and CPU, RAM Energy Info From CodeCarbon!*

## How To Use

1. Check if you installed the libraries and versions that located below.
(If you don't have one of them please install using `pip install`)


```
### About the Library's Version

- codecarbon v3.0.2
- torch in PyTorch 1.12.0a0+02fb0b0f.nv22.06 (It's fit for NVIDIA GPU)
- jtop 4.3.2
- numpy 1.17.4
```

2. Operate gpu_test_workflows.py when you want to check the energy consumption and CO2 emissions of GPU/CPU/RAM

```
python3 gpu_test_workflows.py
```

3. Then you can check the result csv files

<details>
  <summary>CPU & RAM results -> emissions.csv</summary>

  - **GPU Energy (kWh)** → From `jtop`  
    (measured GPU power and converted to energy)  
  - **CPU & RAM CO₂ (kg)** → From `CodeCarbon`  
    (automatic estimation during workload execution)  
  - **Total CO₂ (kg)** → Calculated as `GPU CO₂ + CPU & RAM CO₂`  
  - **GPU Count** → From `jtop`  
    (based on Jetson board model)  
  - **GPU Name** → From `jtop`  
    (mapped from Jetson hardware info)  

</details>

<details>
  <summary>GPU results -> gpu_log.csv</summary>

  - **timestamp** → When the GPU measurement was recorded  
  - **gpu_power_w** → GPU power consumption from `jtop` (watts)  
  - **gpu_energy_kwh** → GPU energy consumed calculated from power measurements (kWh)  
  - **gpu_co2_kg** → GPU CO₂ emissions calculated from energy consumption (kg CO₂)  

</details>

<details>
  <summary>GPU / CPU / RAM results -> total_summary.csv</summary>

  - **timestamp** → When the measurement was recorded  
  - **project_name** → Name of the project being monitored (e.g., "codecarbon")  
  - **run_id** → Unique identifier for each monitoring session  
  - **experiment_id** → Identifier for grouping related runs  
  - **duration** → Time elapsed during the measurement period (seconds)  
  - **emissions** → Total CO₂ emissions for this measurement (kg CO₂)  
  - **emissions_rate** → Rate of CO₂ emissions (kg CO₂ per second)  
  - **cpu_power** → CPU power consumption from CodeCarbon (watts)  
  - **gpu_power** → GPU power consumption from CodeCarbon (watts) - **unreliable/0.0**  
  - **ram_power** → RAM power consumption from CodeCarbon (watts)  
  - **cpu_energy** → CPU energy consumed from CodeCarbon (kWh)  
  - **gpu_energy** → GPU energy consumed from CodeCarbon (kWh) - **unreliable/0.0**  
  - **ram_energy** → RAM energy consumed from CodeCarbon (kWh)  
  - **energy_consumed** → Total energy consumed across all components from CodeCarbon (kWh)  
  - **country_name** → Country where the computation is running  
  - **country_iso_code** → ISO code for the country (e.g., "USA")  
  - **region** → Geographic region (e.g., "california")  
  - **cloud_provider** → Cloud service provider (empty if local)  
  - **cloud_region** → Cloud provider's region (empty if local)  
  - **os** → Operating system information  
  - **python_version** → Python version used  
  - **codecarbon_version** → Version of CodeCarbon library  
  - **cpu_count** → Number of CPU cores  
  - **cpu_model** → CPU model information  
  - **gpu_count** → Number of GPUs detected - **unreliable**  
  - **gpu_model** → GPU model information - **unreliable**  
  - **longitude** → Geographic longitude coordinate  
  - **latitude** → Geographic latitude coordinate  
  - **ram_total_size** → Total RAM size (GB)  
  - **tracking_mode** → CodeCarbon tracking mode (e.g., "machine")  

</details>

---
## Demo

![Demo](custom_codecarbon.gif)



---
### About Calculation → I use the GPU emission Calculation in Same formula!


| CodeCarbon’s CO2 Calculation Method                  | GPU emission Calculation Method               |
|--------------------------|--------------------------|
| ```CO₂ emissions = Energy Consumption × Carbon Intensity```       | ```GPU Energy Calculation (kg) = Power (W) × Time (hours) / 1000```
GPU CO₂ Calculation (kg) = Energy (kWh) × Carbon Intensity (kg CO₂/kWh)    |
|**Carbon Intensity**: Regional grid carbon intensity (kg CO₂/kWh)         | 
