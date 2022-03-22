# raspberry-pi
Code that runs on the raspberry pi. Handles GPIO for buttons, piezoelectric buzzer, and camera. Also makes API calls to the server to perform AI inference tasks.

## Device Setup
First, download [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/). We recommend the 32-bit Raspberry Pi OS Lite for best performance.

Use [balenaEtcher](https://www.balena.io/etcher/) to flash the OS onto a 32GB microSD card.

Navigate to the newly congifured boot drive (remove and reinsert microSD if the boot drive is not visible). Run the following command to enable `ssh`:
```
touch ssh
```
This will allow you to remotely log-in and control the Raspberry Pi.

Then to allow the Raspberry Pi to connect to a Wi-Fi network, create a new file and edit it with the following command:
```
vim wpa_supplicant.conf
```
And copy the following as the contents of the file:
```
country=CA # Your 2-digit country code
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
    ssid="YOUR_NETWORK_NAME"
    psk="YOUR_PASSWORD"
    key_mgmt=WPA-PSK
}
```

Connect the Raspberry Pi to a monitor and keyboard for a one-time setup. And connect it to power. Log-in with the default credentials (assuming a fresh Raspberry Pi OS install). Run the following command to allow cloning of the `raspberry-pi` repository:
```
sudo apt-get install git
```

Then, run the following to get the IP address of the Raspberry Pi on the current Wi-Fi network (should be the same that you used in `wpa_supplicant.conf`):
```
hostname -I
```
This IP address is the one you will use to ssh to the Raspberry Pi.

## Remotely Connecting to the Raspberry Pi
Use the following command to connect to the Raspberry Pi:
```
ssh pi@<IP address>
```

Now you can clone the `raspberry-pi` repository however you like! We recommend [generating an SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and [adding it to your GitHub account.](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

## Module Setup
Most of the libraries needed should come pre-installed with the OS, with the exception of the following:
- opencv
- picamera
- RPi.GPIO

Install opencv with:
```
sudo apt install python3-opencv
```

Install `picamera` with:
```
sudo -H apt install python3-picamera
```
Then enable the camera by entering:
```
sudo raspi-config
```
And navigate to `Interface Options` and select `Legacy Camera` to enable it.

If you are missing `RPi.GPIO`, install with:
```
sudo apt install pigpio
```

Now reboot the Raspberry Pi by entering:
```
sudo shutdown -r now
```

## Running
Before running, ensure the server is up and update `SERVER_URL` if necessary.
```
python3 main.py
```
