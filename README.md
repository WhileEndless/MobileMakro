# MobileMakro

MobileMakro is a web-based tool that automates tasks by executing terminal commands on connected devices or systems. Users can create, edit, and execute macros consisting of terminal commands, making it ideal for automating repetitive tasks and streamlining operations.

## Features

- **Macro Management**: Easily create, edit, and delete macros.
- **Macro Execution**: Send terminal commands as macros to connected devices or systems.
- **Device/System Selection**: Automatically detects and lists connected devices or systems.
- **Step Types**: Supports various macro steps, such as:
  - Text input
  - Terminal commands
  - Key events (e.g., Tab, Enter, Back, Home, etc.)
  - Tap and swipe gestures
- **Screenshot Functionality**: Capture screenshots of the connected device/system.
- **Direct Text Sending**: Quickly send custom text to the connected device/system without needing a macro.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/WhileEndless/MobileMakro.git
   cd MobileMakro
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database and start the application:
   ```bash
   python3 app.py
   ```

## Usage

1. **Run the Application**:
   ```bash
   python3 app.py
   ```

2. **Connect Devices/Systems**: Ensure that your devices or systems are properly connected. The tool will automatically list available devices/systems in the "Select Device" dropdown.

3. **Create Macros**: Use the interface to add steps, including terminal commands, key events, and gestures, to automate tasks.

4. **Execute Macros**: Select a macro and a connected device/system to run the macro.

5. **Take Screenshots**: Capture the screen of connected devices/systems and use it for setting up precise touch gestures (e.g., tap, swipe).

## Macro Creation

Macros are composed of multiple steps, each of which can be a terminal command, key event, or gesture. Example steps include:

- **Text Input**: Send a string of text to the connected device.
- **Terminal Command**: Execute any shell command on the connected system.
- **Key Events**: Simulate keypress events such as Tab, Enter, Back, and Home.
- **Gestures**: Simulate gestures like tap and swipe on touch-based systems.

### Example Macro

- Text: "Automation Started"
- Terminal Command: `ls -la`
- Tap at coordinates (300, 500)

## License

This project is licensed under the MIT License. For more details, visit the [repository](https://github.com/WhileEndless/MobileMakro.git).
