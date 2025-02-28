# Mobile Test Automation Framework

This repository contains a modular and scalable test automation framework for Android applications using Python and Appium.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Appium Server](https://appium.io/docs/en/about-appium/getting-started/)
- [Android SDK](https://developer.android.com/studio)
- Java JDK (required for Android development)
- Node.js (for Appium installation)
- ADB (Android Debug Bridge)
- Git

## Installation

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/lonelyday01/mobile-test-framework.git
   cd mobile-test-framework
   ```

2. **Create a Virtual Environment:**
   ```sh
   python -m venv venv
   # On Mac source venv/bin/activate
   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   Update your environment variables to include paths for Java, Android SDK, and ADB.
   
   Example (Linux/macOS):
   ```sh
   export ANDROID_HOME=$HOME/Library/Android/sdk
   export PATH=$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH
   ```

## Running Tests

### 1. Start the Appium Server
Ensure Appium is running before executing the tests:
```sh
appium
```

### 2. Execute a Test
To run all tests:
```sh
pytest
```
To run a file test
```sh
python -m pytest .\tests\embeeded_apps\calculator\test_calculator.py
```
To run a specific test:
```sh
python -m pytest .\tests\embeeded_apps\calculator\test_calculator.py::test_clear_calculator
```



### 3. Running Tests with Logging and Report Generation
All logs, screenshots, JSON, and HTML reports will be stored in a dedicated folder named according to the test execution.


## Test Report Structure
- **Logs:** Saved inside the execution folder.
- **Screenshots:** Captured on failure and stored in the same folder.
- **JSON Report:** Stored in `reports/<test-case-name>/report.json`.
- **HTML Report:** Generated in `reports/<test-case-name>/report.html`.

## Device Capabilities
Device capabilities are stored in a separate JSON file and can be accessed from anywhere in the project.

Example:
```json
{
  "platformName": "Android",
  "deviceName": "emulator-5554",
  "app": "path/to/app.apk",
  "automationName": "UiAutomator2"
}
```

## Contribution
Feel free to contribute to this project. Please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature-branch-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Create a Pull Request.

## Contact
For any issues, feel free to open an issue or contact the maintainers.

