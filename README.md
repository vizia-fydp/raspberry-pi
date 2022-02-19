# raspberry-pi
Code that runs on the raspberry pi. Handles GPIO for buttons, piezoelectric buzzer, and camera. Also makes API calls to the server to perform AI inference tasks.

## Setup
Most of the libraries needed should come pre-installed with the OS, with the exception of opencv. Install opencv with:
```
sudo apt install python3-opencv
```

If you are missing `RPi.GPIO`, install with:
```
sudo apt install pigpio
```

## Running
Before running, ensure the server is up and update `SERVER_URL` if necessary.
```
python3 main.py
```