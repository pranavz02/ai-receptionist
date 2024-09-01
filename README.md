# AI Receptionist for Dr. Adrin

## Overview

The AI Receptionist is a text-based assistant designed to help users with emergency situations or leave messages for Dr. Adrin. The application uses threading to handle real-time user interactions while querying an emergency response database. It includes a styled welcome message and color-coded responses for an enhanced user experience.

## Features

- **Emergency Handling:** Provides immediate next steps based on the type of emergency described by the user.
- **Message Handling:** Allows users to leave a message for Dr. Adrin.
- **Background Processing:** Utilizes threading to manage database queries and maintain responsive interactions.
- **Styled Outputs:** Employs `pyfiglet` for ASCII art welcome text and `termcolor` for colorized output.
- **Simulated Delay:** Mimics real-world response time with an artificial delay in database queries.

## Installation

### Prerequisites

- Python 3.x
- Libraries: `pyfiglet`, `termcolor`, `inquirer`, `qdrant-client`, `google-generativeai`

### Installing Dependencies

1. **Clone the repository:**

   ```bash
   git clone https://github.com/pranavz02/ai-receptionist.git
   cd ai-receptionist
    ```

2. **Install the required libraries:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**

   ```bash
   python main.py
    ```

2. **Follow the on-screen instructions to interact with the AI Receptionist.**

