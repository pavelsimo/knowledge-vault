# Hailo AI Accelerator

The Hailo-8 is a dedicated AI inference accelerator chip designed for edge deployment, offering high-throughput neural network inference at low power. Setting up a Hailo-based system involves two separate machines: a **client** (ARM/Raspberry Pi running inference via HailoRT) and a **server** (x86_64 machine running the Hailo Dataflow Compiler to compile ONNX models into `.hef` files).

---

## Architecture Overview

| Component | Role | Host |
|-----------|------|------|
| **HailoRT** | Runtime library + PCIe driver for inference | ARM64 (e.g. Raspberry Pi) |
| **Hailo Dataflow Compiler (DFC)** | Compiles ONNX → `.hef` for Hailo-8 | x86_64 Ubuntu |
| **Hailo Model Zoo** | Pre-built model configs (YAML + `.alls`) | x86_64 Ubuntu |
| **`.hef` file** | Compiled hardware-executable model | Deployed to client |

The `.hef` (Hailo Executable Format) is the compiled artifact produced by the Dataflow Compiler and loaded by HailoRT at inference time.

---

## Client Setup (HailoRT — ARM64)

Install HailoRT and the PCIe kernel driver on the inference device.

**Prerequisites:**
- Ubuntu ARM64 with Hailo-8 over PCIe
- Python 3.12
- Packages from the Hailo Developer Zone: `hailort_<version>_<arch>.deb`, `hailort-pcie-driver_<version>_all.deb`, and the Python wheel

### Installation

```shell
export HAILO_VERSION=4.23.0
export HAILO_ARCH=$(dpkg --print-architecture)

sudo dpkg --install \
  hailort_${HAILO_VERSION}_${HAILO_ARCH}.deb \
  hailort-pcie-driver_${HAILO_VERSION}_all.deb

pip install hailort-${HAILO_VERSION}-cp312-cp312-linux_aarch64.whl
pip install -r requirements.txt
```

### Fix PCIe Descriptor Page Size

The default descriptor page size (16384) exceeds the hardware maximum (4096), causing runtime errors. This must be fixed and persisted:

```shell
sudo modprobe -r hailo_pci
sudo modprobe hailo_pci force_desc_page_size=4096
echo "options hailo_pci force_desc_page_size=4096" | sudo tee /etc/modprobe.d/hailo_pci.conf
```

> Source: [Hailo community fix for `max_desc_page_size` error](https://community.hailo.ai/t/hailort-error-check-failed-max-desc-page-size-given-16384-is-bigger-than-hw-max-desc-page-size-4096/3690/3)

---

## Server Setup (Dataflow Compiler — x86_64)

Compile an ONNX model into a `.hef` file for Hailo-8.

**Prerequisites:**
- Ubuntu x86_64
- Python 3.10
- At least **1024 calibration images** (required for post-training quantization)
- Wheels from Hailo Developer Zone: `hailo_dataflow_compiler-3.33.1-py3-none-linux_x86_64.whl`, `hailo_model_zoo-2.18.0-py3-none-any.whl`

### Installation

```shell
sudo apt-get install -y cmake python3.10 python3.12-venv python3.10-dev \
  python3-tk graphviz libgraphviz-dev pkg-config

python3.10 -m venv .venv
source .venv/bin/activate

pip install hailo_dataflow_compiler-3.33.1-py3-none-linux_x86_64.whl
pip install hailo_model_zoo-2.18.0-py3-none-any.whl
```

### Compile a Model

```shell
hailomz compile \
  --ckpt best.onnx \
  --hw-arch hailo8 \
  --classes 3 \
  --calib-path /path/to/calibration/images/ \
  --yaml .venv/lib/python3.10/site-packages/hailo_model_zoo/cfg/networks/yolo26n.yaml
```

### Fix Calibration Images (EXIF / Colorspace Issues)

Some images fail calibration due to EXIF orientation metadata or non-RGB colorspaces. Strip and normalize:

```shell
mkdir -p /tmp/hailo_calib_clean
find ./train/images/ -type f | while read -r f; do
  base="$(basename "${f%.*}")"
  convert "$f" -auto-orient -strip -alpha off -colorspace sRGB "/tmp/hailo_calib_clean/${base}.jpg"
done
```

---

## Key Concepts

- **Post-training quantization (PTQ):** The Hailo DFC quantizes the model during compilation using calibration images to minimize accuracy loss. At least 1024 images are required.
- **`.alls` config:** Controls compilation parameters (e.g. `calib-size`). Found under `hailo_model_zoo/cfg/alls/`.
- **`hailomz`:** CLI entry point for the Hailo Model Zoo; wraps DFC with model-specific YAML configs.
- **HailoRT Python bindings:** Allow inference calls directly from Python on the client device.

---

## Related Topics

- [[physical-ai]] — Hailo-8 is commonly used in edge robotics and Physical AI deployment pipelines
- [[robot-learning]] — Inference acceleration is key for real-time robot perception
- [[object-detection]] — YOLO models (e.g. `yolo26n`) are a primary use case for Hailo compilation
- [[quantization]] — The DFC performs PTQ; understanding quantization error helps tune calibration
- [[gpu-cuda]] — Contrast with CUDA-based GPU inference for cloud/server deployments
