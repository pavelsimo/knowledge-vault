# Hailo Client Setup (HailoRT)

Guide for installing HailoRT and the PCIe driver on the target device (e.g. Raspberry Pi or ARM-based host) that runs inference with the Hailo-8 accelerator.

**Reference:** https://hailo.ai/developer-zone/documentation/hailort-v4-23-0/?sp_referrer=install/install.html#installation-on-ubuntu

---

## Prerequisites

- Ubuntu ARM64 device with Hailo-8 connected over PCIe
- Python 3.12
- Debian packages and wheel downloaded from the Hailo Developer Zone:
  - `hailort_<version>_<arch>.deb`
  - `hailort-pcie-driver_<version>_all.deb`
  - `hailort-<version>-cp312-cp312-linux_aarch64.whl`

---

## 1. Install HailoRT and PCIe Driver

```shell
export HAILO_VERSION=4.23.0
export HAILO_ARCH=$(dpkg --print-architecture)

sudo dpkg --install \
  hailort_${HAILO_VERSION}_${HAILO_ARCH}.deb \
  hailort-pcie-driver_${HAILO_VERSION}_all.deb
```

## 2. Install Python Bindings and Requirements

```shell
pip install hailort-${HAILO_VERSION}-cp312-cp312-linux_aarch64.whl
pip install -r requirements.txt
```

## 3. Fix PCIe Descriptor Page Size

The Hailo PCIe driver defaults to a descriptor page size that may exceed the hardware maximum (4096 bytes), causing runtime errors. Apply the fix and persist it across reboots:

```shell
sudo modprobe -r hailo_pci
sudo modprobe hailo_pci force_desc_page_size=4096
echo "options hailo_pci force_desc_page_size=4096" | sudo tee /etc/modprobe.d/hailo_pci.conf
```

> **Reference:** https://community.hailo.ai/t/hailort-error-check-failed-max-desc-page-size-given-16384-is-bigger-than-hw-max-desc-page-size-4096/3690/3
