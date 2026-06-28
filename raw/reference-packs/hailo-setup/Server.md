# Hailo Server Setup (Dataflow Compiler)

Guide for installing the Hailo Dataflow Compiler and compiling an ONNX model into a `.hef` file for the Hailo-8 accelerator.

**Reference:** https://hailo.ai/developer-zone/documentation/dataflow-compiler-v3-33-1/?sp_referrer=install/install.html

---

## Prerequisites

- Ubuntu x86_64 machine
- Python 3.10
- At least 1024 calibration images available locally
- Wheel files downloaded from the Hailo Developer Zone:
  - `hailo_dataflow_compiler-3.33.1-py3-none-linux_x86_64.whl`
  - `hailo_model_zoo-2.18.0-py3-none-any.whl`

---

## 1. Install System Dependencies

```shell
sudo apt update
sudo apt-get install -y cmake
sudo apt-get install -y python3.10 python3.12-venv python3.10-dev
sudo apt-get install -y python3-tk graphviz libgraphviz-dev pkg-config
```

## 2. Create Python Virtual Environment

```shell
python3.10 -m venv .venv
source .venv/bin/activate
```

## 3. Install Hailo Packages

```shell
pip install hailo_dataflow_compiler-3.33.1-py3-none-linux_x86_64.whl
pip install hailo_model_zoo-2.18.0-py3-none-any.whl
```

## 4. (Optional) Adjust Calibration Size

Edit the `.alls` config to set the `calib-size` parameter before compiling:

```shell
nano .venv/lib/python3.10/site-packages/hailo_model_zoo/cfg/alls/generic/yolo26n.alls
```

## 5. (Optional) Fix Calibration Images

Some images may have EXIF orientation issues or be in an incompatible colorspace. Strip metadata and normalize to RGB:

```shell
mkdir -p /tmp/hailo_calib_clean
find ../../datasets/processed/v1/train/images/ -type f | while read -r f; do
  base="$(basename "${f%.*}")"
  convert "$f" -auto-orient -strip -alpha off -colorspace sRGB "/tmp/hailo_calib_clean/${base}.jpg"
done
```

## 6. Compile Model

> **Note:** At least 1024 calibration images are required for the calibration step.

```shell
hailomz compile \
  --ckpt best.onnx \
  --hw-arch hailo8 \
  --classes 3 \
  --calib-path ../../datasets/processed/v1/train/images/ \
  --yaml .venv/lib/python3.10/site-packages/hailo_model_zoo/cfg/networks/yolo26n.yaml
```
