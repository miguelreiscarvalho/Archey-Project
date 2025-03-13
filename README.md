

# Archey

## Hi, everyone
I come with great enthusiasm to present to you this project, which aims to provide a solution that improves the lives of people with motor limitations due to hereditary diseases or physical trauma related to the loss or absence of upper limbs. These conditions impose significant restrictions on their daily lives, particularly when using tools like computers and laptops, often requiring external assistance.

With this solution, I offer a diversified and personalized experience—the ability to control these devices using only facial gestures and expressions.

## 📌 Requirements

Here is the list of prerequisites for using the software.

- **Webcam** (Essential feature, ensure that a webcam is installed on your machine to enable recognition and proper software operation).
- You need to have at least a computer with intermediate specifications, so it can run multiple software applications that use a moderate amount of RAM. This way, the software can deliver better performance and ensure smooth operation.
- Install the third-party software **[Virtual Keyboard](https://apps.microsoft.com/detail/9NBLGGH35MPC?hl=en&gl=US)**, which allows you to type without using a physical keyboard. 

REQUIREMENTS FOR OPERATION
Required Software:
- IDE for code execution (PyCharm or Visual Studio Code)
- [Python 3.8x](https://www.python.org/)
- [Java JDK](https://www.oracle.com/java/technologies/downloads/) latest version.
- 
## 🚀 Installation

Steps to install the project:

```bash
- It will be necessary to create a virtual machine in the IDE.

Installation:
# Run each line below one at a time

pip install opencv-python
pip install numpy
pip install mediapipe
pip install pynput
pip install pyautogui
pip install deepface

```
## 🛠 Usage
To run the project, you must have a webcam installed and positioned as centrally as possible with your face. Try checking this by opening the pre-installed "Camera" software on your computer to ensure your face is as aligned as possible with the webcam.

If you have more than one webcam, you will need to select which one will be used for the software. To do this, go through the algorithm script and look for the following line of code:

```bash
# Change the default key value from 0 to another value above it. For example: 1, 2, 3...
cap = cv.VideoCapture(0)
```

## Facial Gesture Commands:

- **Click** - Raise eyebrows
- **Double Click** - Hold raised eyebrows
- **Press and Hold** - Open mouth
- **Right Click** - Smile

The movement of the mouse across the computer screen functions similarly to a video game joystick, where you need to move it in a certain direction to perform an action. In this case, your face will act as the joystick, and by moving your head, the cursor will respond by following the same direction as your face.

When you run the software, a tab containing your webcam image will open on the computer. Don't worry; it won't interfere with using the program. Whenever the cursor passes over the tab, it will automatically move to another corner of the screen.

This tab has several points that mark specific parts of your face and will follow your movements.

## **The Points**
Most of the points drawn are used to detect the movements made on your face and, consequently, the desired facial expressions.

### **Nose**
The point represented at the tip of the nose acts as the joystick pointer and is responsible for controlling the mouse position. Notice that there is a square right in the center of the tab showing your face; the area inside this square is called the "dead zone," where the mouse does not move, and facial expressions are verified. This means the mouse will only move if you move the point drawn on the nose outside the square. Additionally, the facial expressions responsible for performing other mouse functions are only executed when the nose point is inside this square. Therefore, when it is outside, other mouse functions will be blocked for safety reasons and to ensure the software operates smoothly, preventing unwanted actions.

