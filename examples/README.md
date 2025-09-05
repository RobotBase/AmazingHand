# AmazingHand Examples

This directory contains example scripts demonstrating various features of the AmazingHand SDK.

## Available Examples

### 1. `single_finger_control.py`
Demonstrates basic single finger control functionality.

### 2. `custom_gesture.py`
Shows how to create custom gestures by combining individual finger movements.

### 3. `gesture_sequence.py`
Demonstrates how to execute a sequence of predefined gestures.

### 4. `data_reading_test.py`
**New!** Comprehensive test of the bidirectional communication features:
- Real-time sensor data reading (position, speed, load, voltage, temperature)
- Static and dynamic status monitoring
- Gesture testing with sensor feedback

### 5. `sensor_monitoring.py`
**New!** Real-time motor monitoring and sensor data visualization:
- Continuous motor status monitoring
- Individual motor data reading
- Performance monitoring during gesture execution

## Key Features Demonstrated

### Basic Control
- Individual finger control (index, middle, ring, thumb)
- Predefined gestures (open, close, point, victory, ok, pinch)
- Speed and angle control

### Advanced Features (New)
- **Bidirectional Communication**: Read motor status in real-time
- **Sensor Data**: Position, speed, load, voltage, and temperature monitoring
- **Real-time Feedback**: Monitor hand performance during movement
- **Error Handling**: Robust error detection and reporting

## Usage

Before running any example, make sure to:

1. Update the `PORT` variable with your AmazingHand's actual serial port
2. Install required dependencies:
   ```bash
   pip install amazingctrl
   ```

3. Run any example:
   ```bash
   python examples/data_reading_test.py
   ```

## Hardware Requirements

- AmazingHand robotic hand
- USB connection to computer
- Compatible servo motors (8 total)

## Important Notes

- Always call `hand.start()` before using the hand
- Always call `hand.stop()` when finished to safely disable motors
- The sensor reading features require the updated amazingctrl package with bidirectional communication support
