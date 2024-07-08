# BlinkTalk

BlinkTalk is a computer vision project designed to help quadriplegic patients communicate by detecting eye blinks and translating them into Morse code, which is then converted into English text.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Real-time eye blink detection using a webcam.
- Translation of eye blinks into Morse code.
- Conversion of Morse code into English text.
- Visual feedback on detected Morse code and translated text.

## Technologies

- Python
- OpenCV
- Dlib
- Scipy
- Numpy

## Installation

### Prerequisites

- Python 3.6+
- A webcam

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/BlinkTalk.git
    cd BlinkTalk
    ```

2. Install the required Python packages:

    ```bash
    pip install opencv-python dlib scipy numpy
    ```

3. Download the dlib facial landmark predictor model:

    - [shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
    - Extract the file and place `shape_predictor_68_face_landmarks.dat` in the project directory.

## Usage

1. Ensure your webcam is connected and working.
2. Run the main script:

    ```bash
    python blink_talk.py
    ```

3. The program will start the webcam feed. Blink to input Morse code:
    - Short blink for `.` (dot)
    - Long blink for `-` (dash)

4. The translated English text will be displayed on the screen.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [OpenCV](https://opencv.org/)
- [Dlib](http://dlib.net/)
- [Scipy](https://www.scipy.org/)
- [Numpy](https://numpy.org/)

