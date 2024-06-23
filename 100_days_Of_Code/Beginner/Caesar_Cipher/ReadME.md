🔐 This project is a simple implementation of the Caesar Cipher, a basic encryption technique where each letter in the plaintext is shifted a certain number of places down or up the alphabet.

Features
🛡️ Encoding: Encrypt a message by shifting letters forward in the alphabet.
🔓 Decoding: Decrypt a message by shifting letters backward in the alphabet.
🤖 User Interaction: Continues to ask the user if they want to encode/decode more messages until they choose to exit.
How to Use
▶️ Run the Program: When the program starts, it will display a logo (imported from art.py) and prompt the user to either encode or decode a message.
🖊️ User Input:
Enter encode to encrypt a message or decode to decrypt a message.
Type the message you want to encode or decode.
Enter the shift number (the number of places each letter in the message will be shifted).
➗ Shift Calculation: The program handles shift values greater than 26 by using the modulus operator to ensure the shift wraps around the alphabet.
📬 Output: The program will display the encoded or decoded message.
🔁 Repeat or Exit: The program will ask if you want to run another cipher operation. Type yes to continue or no to exit.