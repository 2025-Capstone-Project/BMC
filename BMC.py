import psutil
import cpuinfo
import GPUtil
import platform
import os

# CPU 정보
def get_cpu_info():
    os_type = platform.system()
    
    if os_type == 'Linux':
        try:
            temps = []
            base_dir = '/sys/class/thermal/'
            for zone in os.listdir(base_dir):
                if zone.startswith('thermal_zone'):
                    with open(f'{base_dir}{zone}/temp', 'r') as f:
                        temp = float(f.read().strip()) / 1000.0  # 밀리섭씨 -> 섭씨
                        temps.append(temp)
            if temps:
                return round(sum(temps) / len(temps) ,2)  # 평균 온도 반환
            return "온도 정보를 찾을 수 없습니다."
        except:
            return "Linux 온도 정보 접근 실패"
            
    elif os_type == 'Windows':
        try:
            import wmi
            w = wmi.WMI(namespace="root\\wmi")
            temperature_info = w.Win32_TemperatureProbe()[0]
            return temperature_info.CurrentReading
        except Exception as e:
            return "Windows 온도 정보 접근 실패: " + str(e)
            
    elif os_type == 'Darwin':  # macOS
        try:
            import subprocess
            result = subprocess.run(['sudo', 'powermetrics', '--samplers', 'smc', '-n', '1'], 
                                   capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'CPU die temperature' in line:
                    return float(line.split(':')[1].strip().rstrip(' C'))
            return "macOS 온도 정보를 찾을 수 없습니다."
        except:
            return "macOS 온도 정보 접근 실패"
    
    return "지원되지 않는 운영체제입니다."

# RAM 사용량
def get_ram_info():
    ram = psutil.virtual_memory()
    return {
        "총 메모리": f"{ram.total / (1024**3):.2f} GB",
        "사용 중인 메모리": f"{ram.used / (1024**3):.2f} GB",
        "사용 가능한 메모리": f"{ram.available / (1024**3):.2f} GB",
        "사용률": f"{ram.percent}%"
    }

# GPU 정보
def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = []
        
        for i, gpu in enumerate(gpus):
            gpu_info.append({
                "GPU ID": i,
                "이름": gpu.name,
                "부하율": f"{gpu.load * 100:.2f}%",
                "메모리 사용": f"{gpu.memoryUsed} MB / {gpu.memoryTotal} MB",
                "메모리 사용률": f"{gpu.memoryUtil * 100:.2f}%",
                "온도": f"{gpu.temperature}°C"
            })
            
        if not gpu_info:
            return "GPU를 찾을 수 없습니다."
        
        return gpu_info
    except:
        return "GPU 정보 접근 실패"

# 모든 정보 출력
def print_system_info():
    print("=" * 50)
    print("시스템 정보")
    print("=" * 50)
    
    # CPU 정보
    print("\n[CPU 정보]")
    print(f"CPU 모델: {cpuinfo.get_cpu_info()['brand_raw']}")
    print(f"코어 수: {psutil.cpu_count(logical=False)} (물리적), {psutil.cpu_count(logical=True)} (논리적)")
    print(f"CPU 사용률: {psutil.cpu_percent()}%")
    print(f"CPU 온도: {get_cpu_info()}°C")
    
    # RAM 정보
    print("\n[RAM 정보]")
    ram_info = get_ram_info()
    for key, value in ram_info.items():
        print(f"{key}: {value}")
    
    # GPU 정보
    print("\n[GPU 정보]")
    gpu_info = get_gpu_info()
    if isinstance(gpu_info, list):
        for i, gpu in enumerate(gpu_info):
            print(f"\nGPU {i+1}:")
            for key, value in gpu.items():
                if key != "GPU ID":
                    print(f"  {key}: {value}")
    else:
        print(gpu_info)
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    print_system_info()
