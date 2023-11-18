# OpenRGB

![OpenRGB](../images/openrgb.png)

OpenRGB is a unified interface for managing RGB hardware and peripherals such as keyboards, case fans, headsets, etc.

OpenRGB supports a variety of devices, check the [OpenRGB website](https://openrgb.org) for detailed compatibility info.

## I2C/SMBus Initialization Errors

Some devices may not be detected if the `i2c_dev` kernel module is not loaded.

If OpenRGB displays warning messages regarding i2c, you can load the `i2c_dev` kernel module with:

```bash
sudo modprobe i2c_dev
```
