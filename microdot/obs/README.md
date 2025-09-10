# Virtual camera

Requires a V4L loopback kernel module.

    > sudo apt install v4l2loopback-dkms

    > cat /etc/modprobe.d/obs.conf
    options v4l2loopback exclusive_caps=1 card_label='OBS Virtual Camera'

    > cat /etc/modules-load.d/obs.conf
    v4l2loopback


# Screen capture


Uses PipeWire anre Requires xdg-desktop-portal.   If these aren't installed
then you need to re-log-in.

    > sudo apt install xdg-desktop-portal-wlr pipewire pipewire-pulse
    > systemctl --user enable pipewire
    > systemctl --user enable pipewire-pulse
