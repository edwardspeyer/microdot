```
> sudo apt install v4l2loopback-dkms

> cat /etc/modprobe.d/obs.conf
options v4l2loopback exclusive_caps=1 card_label='OBS Virtual Camera'

> cat /etc/modules-load.d/obs.conf
v4l2loopback
```
