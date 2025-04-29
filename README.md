# BMC (Basic Monitoring Client)

BMC는 다양한 운영 체제에서 CPU, RAM, GPU의 상태를 모니터링하는 간단한 Python 도구입니다. 하드웨어 정보, 사용률, 온도 등의 시스템 정보를 실시간으로 확인할 수 있습니다.

## 기능

- **CPU 모니터링**: 
  - CPU 모델 정보
  - 물리적/논리적 코어 수
  - CPU 사용률
  - CPU 온도 (OS별 지원)

- **RAM 모니터링**:
  - 총 메모리 용량
  - 사용 중인 메모리
  - 사용 가능한 메모리
  - 메모리 사용률(%)

- **GPU 모니터링** (NVIDIA GPU 지원):
  - GPU 이름
  - GPU 부하율
  - 메모리 사용량
  - 메모리 사용률
  - GPU 온도

## 설치 방법

### 필수 라이브러리

```bash
pip install psutil py-cpuinfo GPUtil wmi
```

### 운영체제별 특이사항

- **Windows**: WMI 라이브러리를 사용하여 온도 정보 수집
- **Linux**: `/sys/class/thermal/` 경로에서 온도 정보 수집
- **macOS**: `powermetrics` 명령어를 통해 온도 정보 수집 (관리자 권한 필요)

## 사용 방법

```bash
python BMC.py
```

실행하면 콘솔에 시스템 정보가 표시됩니다.

## 알려진 문제점

1. **Windows 온도 측정**: 일부 Windows 시스템에서는 WMI를 통한 온도 측정이 지원되지 않을 수 있습니다. 시스템 구성에 따라 다음과 같은 오류가 발생할 수 있습니다:
   - `OLE error 0x80041003`: 지원되지 않는 WMI 네임스페이스
   - `Win32_TemperatureProbe` 클래스 접근 실패

2. **macOS 온도 측정**: `powermetrics` 명령어 실행을 위해 관리자 권한이 필요합니다.

## 시스템 요구사항

- Python 3.6 이상
- Windows, Linux 또는 macOS
- NVIDIA GPU (GPU 모니터링 기능 사용 시)

## 커스터마이징

특정 기능만 사용하려면 BMC.py 파일에서 다음 함수를 개별적으로 호출할 수 있습니다:

- `get_cpu_info()`: CPU 온도 정보
- `get_ram_info()`: RAM 사용 정보
- `get_gpu_info()`: GPU 상태 정보
- `print_system_info()`: 모든 정보 출력
