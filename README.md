# EEE4113F_Group34_MDLPRI040_PLLKAS005_SNGLIY001
EEE4113F Engineering Design - Group 34 - Remote Pulse Oximeter Project

- Overview:
Project CODY is a remote pulse oximeter system designed specifically for monitoring the health of penguins in the wild. The system captures and transmits vital physiological data—such as blood oxygen levels and heart rate—along with GPS coordinates to assist researchers in studying penguin behavior and health in their natural habitat.

- Key Features:
Remote Monitoring: Wireless transmission of physiological (heart rate and oxygen saturation) data in real-time.
GPS Tracking: Real-time location tracking of the penguin.
Pulse Oximetry: Non-invasive measurement of blood oxygen saturation and heart rate.
Data Visualization: Front-end GUI for data display and analysis.
Portable Design: Custom-designed housing suitable for penguin attachment, designed for durability and lightweight use.

- Project Structure:
This repository contains:
Firmware for microcontroller and sensors.
Signal processing and data handling scripts.
Front-end application (PyQt5-based GUI).
3D printable housing design files.
Documentation and system diagrams.

- Roles and Contributions:

  Liyana Singh (SNGLIY001) – Subsystem 1 - Circuit Design
  Designed and implemented the analog front-end circuitry for the IR sensor.

  Priya Moodley (MDLPRI040) – Subsystem 2 - Microcontroller, GPS, and Signal Processing
  Programmed the ESP32 microcontroller for data acquisition. Integrated GPS module for coordinate tracking. Applied signal processing techniques for clean, interpretable oximetry and     pulse data. Developed the power management system. 

  Kashan Pillay (PLLKAS005) – Subsystem 3 - Front-End Development, Data Analysis, and Housing Design
  Built a PyQt5 GUI for data visualization and system interaction. Developed tools for logging and analyzing collected data. Designed and 3D printed the custom housing suitable for       penguin use.

