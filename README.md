# Snake Game Keylogger - Hidden Threat Demo

![Snake Game Keylogger](path/to/your/image.jpg)

## Overview

This project demonstrates how a keylogger can be embedded within a seemingly harmless Snake game to capture and exfiltrate sensitive data from a victim's machine. The demo showcases the techniques used to hide the malicious code, capture input data, and send it to an attacker via Telegram.

## How It Works

1. **Phising the victim through GMAIL**
   - The keylogger code is injected into the Snake game, designed to start capturing keystrokes as soon as the game begins.
   ![Victim's machine](https://github.com/user-attachments/assets/cd290938-571e-4297-b0de-ce8a003ac599)

   - After extract the zip file:
   ![After extract](https://github.com/user-attachments/assets/53d318e9-3702-47f2-8c90-87adaf3f5ca6)

2. **Running the Game:**
   - The victim plays the Snake game without realizing that their inputs are being recorded.
   ![Running game](https://github.com/user-attachments/assets/96e8d664-900e-415a-b737-3c175618a407)

3. **Capturing and Exfiltrating Data:**
   - The captured keystrokes are stored.
   ![Log text](https://github.com/user-attachments/assets/74b6849e-6a06-4e3f-ba8a-33d429287a2f)

   - Password stored in Google Chrome also be stealed.
   ![Chrome data](https://github.com/user-attachments/assets/c438598d-4fa0-46af-9064-750528b3a70f)

3. **Adding Keylogger to Startup**
   - To ensure persistence, the keylogger script is added to the startup folder, making it execute each time the victim’s system is restarted.
   ![Add keylogger to startup folder](https://github.com/user-attachments/assets/a403c99b-28e5-4a45-9815-cccbe6878fa9)

5. **Data Transmission:**
   - The data is sent securely and stealthily to the attacker's Telegram bot, and ensuring the attacker receives the information without the victim's knowledge.
   ![Send to attacker](https://github.com/user-attachments/assets/964bb31f-18ee-4bff-b0a1-858d33f75aca)

## Setup

To run this project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/Matth3wV0/Keylogger.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Snake game with the embedded keylogger:
   ```bash
   python snake_game_keylogger.py
   ```
4. Monitor the data being sent to the attacker's Telegram bot.

## DISCLAIMER

This project is intended for educational and research purposes only. The techniques demonstrated should not be used for illegal or unethical activities. Always obtain proper authorization before conducting security testing on any system.

