# Snake Game Keylogger - Hidden Threat Demo
![Game](https://github.com/user-attachments/assets/642b780e-9e48-4770-b725-638c23f6db8a)

## Overview

This project demonstrates how a keylogger can be embedded within a seemingly harmless Snake game to capture and exfiltrate sensitive data from a victim's machine. The demo showcases the techniques used to hide the malicious code, capture input data, and send it to an attacker via Telegram.

## How It Works

1. **Phising the victim through MAIL**
   - The keylogger code is injected into the Snake game, designed to start capturing keystrokes as soon as the game begins.
   ![Mail](https://github.com/user-attachments/assets/d5a133d7-0f86-4d15-9e09-a6dc05ae1965)

2. **Running the Game:**
   - The victim plays the Snake game without realizing that their inputs are being recorded.
   ![Running game](https://github.com/user-attachments/assets/96e8d664-900e-415a-b737-3c175618a407)

3. **Capturing and Exfiltrating Data:**
   - The captured keystrokes are stored.
   ![Log text](https://github.com/user-attachments/assets/1a6310fd-b6ca-4ce3-b672-f8a262e38e54)

   - Password stored in Google Chrome also be stealed.
   ![Chrome data](https://github.com/user-attachments/assets/e1a4987b-d4f3-41e8-adc1-6c3cedd393b8)

3. **Adding Keylogger to Startup**
   - To ensure persistence, the keylogger script is added to the startup folder, making it execute each time the victim’s system is restarted.
   ![Add keylogger to startup folder](https://github.com/user-attachments/assets/0db6fb7b-6aa9-4c57-824b-ca3527a5ff51)

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

