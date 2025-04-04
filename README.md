# E-ink Raspberry Pi Clock

This is a simple e-ink raspberry pi zero clock with date and current weather.

<img src="./Images/clock.jpg" alt="Test Run of Code" width="400"/>

## References

The following existing projects/reddit posts were used as reference, starting point, and inspiration for this work and are given credit here:

- [I made a basic clock with a pi zero and an e-ink display](https://www.reddit.com/r/raspberry_pi/comments/vi2xow/i_made_a_basic_clock_with_a_pi_zero_and_an_eink/)
- [Raspberry Pi project ideas: e-ink calendar and clock](https://picockpit.com/raspberry-pi/raspberry-pi-project-ideas-e-ink-calendar-clock/)
- [E-paper Calendar using RPI Zero W - CalDAV support](https://www.reddit.com/r/raspberry_pi/comments/v4ub12/epaper_calendar_using_rpi_zero_w_caldav_support/)
- [Raspberry Pi E-Ink Weather Station using Python](https://learn.adafruit.com/raspberry-pi-e-ink-weather-station-using-python/weather-station-code)
- [Real-Time Weather with Raspberry Pi 4](https://www.hackster.io/gatoninja236/real-time-weather-with-raspberry-pi-4-ad621f)

## Hardware

The following hardware was used:

- [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- [Pi Zero Case for Waveshare 2.13" eInk Display](https://thepihut.com/products/pi-zero-case-for-waveshare-2-13-eink-display)
- [E-Ink Display pHAT - 2.13" (250x122)](https://thepihut.com/products/eink-display-phat-2-13-250x122)
- [CanaKit 5V 2.5A Raspberry Pi 3 B+ Power Supply/Adapter](https://www.amazon.com/dp/B00MARDJZ4)
- SD card

### SD Card Setup

Raspberry Pi OS Lite 64-bit was used for this project. This allow operating the Raspberry Pi Zero in headless mode via SSH access.

1. Download and install Raspberry Pi Imager: https://www.raspberrypi.com/software/
2. Follow steps to install Raspberry Pi OS Lite 64-bit with SSH access and Wifi Enabled
    - I followed this guide: https://peppe8o.com/install-raspberry-pi-os-lite-in-your-raspberry-pi/ 

### Case Setup

1. Assemble case and boards per instructions here: https://thepihut.com/blogs/raspberry-pi-tutorials/pi-zero-case-for-waveshare-2-13-eink-display-assembly-instructions
    - Note: Be sure to insert the SD card before assembling the board into the case as it's much easier than after it's assembled

<img src="./Images/case1.jpg" alt="case setup" width="400"/>

## Raspberry Pi Configuration

Once the SD card is programmed and the case/boards assembled verify boot and access via SSH. Again I followed this guide to establish the connection and update the OS/packages: https://peppe8o.com/install-raspberry-pi-os-lite-in-your-raspberry-pi/

### Library Setup

Follow the Waveshare guide here to configure the OS and install the needed libraries for the e-ink display: https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi

- Note: I also had to install the following tools not directly specified in the Waveshark directions

        sudo apt install swig python3-dev python3-setuptools git

- Note: I did not install wiringPi as it's no longer maintained by the original creator as seems deprecated now?

After installation I was able to run the python demo code and see the e-ink display function.

## GitHub Code Setup

1. Pull down the github code repo to the device home folder: https://github.com/sannong/eink_clock
2. Copy the "lib" and "pic" folders from the Waveshare library to the same folder as the github project (so they are at the same folder level as the eink.py file)
    - These are located at ~/e-Paper/RaspberryPi_JetsonNano/python in the default Waveshare library installation

### Additional Python Libraries

Install the following additional python libraries

        apt-get instal python3-dotenv

### OpenweatherMap API

The weather data uses the OpenweatherMap API to get the current temperature and weather type. A unique OpenweatherApp key must be created by the developer in order to access the API.

- The OpenweatherMap API key and documentation is here: https://openweathermap.org/api. 
- See this for more information on API keys and settings [Real-Time Weather with Raspberry Pi 4](https://www.hackster.io/gatoninja236/real-time-weather-with-raspberry-pi-4-ad621f)

### .env File

To preserve security a local .env file is used to maintain the OpenweatherMap API key, zip code, and locale. A .env file must be created in the same directory as the python script and contains the following where the developer must fill in the appropriate values for each field.

        # .env file
        WEATHER_API_KEY = "<api key>"
        ZIP_CODE = "<zip code>"
        LOCAL = "<locale>"
        
### Test Run

Run the code and see if it works! Press ctrl+c to terminate (the script will clean up and reset the display before terminating so give it a second after pressing ctrl+c)

        python eink.py

### Auto-Run

To make the script auto-run at boot I created a cron job as follows:

1. Give the following command to open the crontab

        crontab -e

2. In the crontab editor add the following line at the bottom (adjusting the path as needed for a particular install)

        @reboot python ~/eink_clock/eink.py &

3. Save the file and reboot.
