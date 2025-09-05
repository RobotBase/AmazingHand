import time
import numpy as np
from rustypot import Scs0009PyController

class AmazingHand:
    def __init__(self, port, side=1, calibration_data=None):
        """
        Initializes the AmazingHand controller.

        :param port: The serial port for communication (e.g., "COM3" or "/dev/tty.usbmodemXXXX").
        :param side: 1 for Right Hand (default), 2 for Left Hand.
        :param calibration_data: A list of 8 calibration values for the servos.
        """
        self.port = port
        self.side = side
        self.controller = Scs0009PyController(
            serial_port=self.port,
            baudrate=1000000,
            timeout=0.5,
        )
        
        if calibration_data:
            self.calibration_data = calibration_data
        else:
            # Default calibration data
            self.calibration_data = [3, 0, -5, -8, -2, 5, -12, 0]

        # Constants
        self.MAX_SPEED = 7
        self.CLOSE_SPEED = 3

    def start(self):
        """
        Starts the connection and enables torque for all motors.
        """
        # In a real scenario, you might need to check the connection status.
        # For now, we assume the connection is successful if no exception is raised.
        for i in range(1, 9):
            self.controller.write_torque_enable(i, 1)
            time.sleep(0.01) # Small delay between commands
        print("AmazingHand started and torque enabled.")

    def stop(self):
        """
        Disables torque for all motors and closes the connection.
        """
        for i in range(1, 9):
            self.controller.write_torque_enable(i, 3) # Use 3 to free the motors
            time.sleep(0.01)
        # The rustypot library doesn't have an explicit close() method,
        # but disabling torque is the main safety action.
        print("AmazingHand stopped and torque disabled.")

    def _move_finger(self, motor_ids, angles, speed):
        """
        Internal helper function to move a finger's servos.
        """
        motor1_id, motor2_id = motor_ids
        angle1, angle2 = angles
        cal_offset1, cal_offset2 = self.calibration_data[motor1_id-1], self.calibration_data[motor2_id-1]

        self.controller.write_goal_speed(motor1_id, speed)
        self.controller.write_goal_speed(motor2_id, speed)
        
        pos1 = np.deg2rad(cal_offset1 + angle1)
        pos2 = np.deg2rad(cal_offset2 + angle2)

        self.controller.write_goal_position(motor1_id, pos1)
        self.controller.write_goal_position(motor2_id, pos2)
        time.sleep(0.005) # Short delay to ensure commands are sent

    def index(self, angle_1, angle_2, speed):
        self._move_finger([1, 2], [angle_1, angle_2], speed)

    def middle(self, angle_1, angle_2, speed):
        self._move_finger([3, 4], [angle_1, angle_2], speed)

    def ring(self, angle_1, angle_2, speed):
        self._move_finger([5, 6], [angle_1, angle_2], speed)

    def thumb(self, angle_1, angle_2, speed):
        self._move_finger([7, 8], [angle_1, angle_2], speed)

    # --- Pre-defined Gestures ---

    def open(self):
        self.index(-35, 35, self.MAX_SPEED)
        self.middle(-35, 35, self.MAX_SPEED)
        self.ring(-35, 35, self.MAX_SPEED)
        self.thumb(-35, 35, self.MAX_SPEED)

    def close(self):
        self.index(90, -90, self.CLOSE_SPEED)
        self.middle(90, -90, self.CLOSE_SPEED)
        self.ring(90, -90, self.CLOSE_SPEED)
        self.thumb(90, -90, self.CLOSE_SPEED + 1)

    def point(self):
        self.index(-40, 40, self.MAX_SPEED)
        self.middle(90, -90, self.MAX_SPEED)
        self.ring(90, -90, self.MAX_SPEED)
        self.thumb(90, -90, self.MAX_SPEED)

    def victory(self):
        if self.side == 1: # Right Hand
            self.index(-15, 65, self.MAX_SPEED)
            self.middle(-65, 15, self.MAX_SPEED)
        else: # Left Hand
            self.index(-65, 15, self.MAX_SPEED)
            self.middle(-15, 65, self.MAX_SPEED)
        self.ring(90, -90, self.MAX_SPEED)
        self.thumb(90, -90, self.MAX_SPEED)

    def ok(self):
        if self.side == 1: # Right Hand
            self.index(50, -50, self.MAX_SPEED)
            self.middle(0, 0, self.MAX_SPEED)
            self.ring(-20, 20, self.MAX_SPEED)
            self.thumb(65, 12, self.MAX_SPEED)
        else: # Left Hand
            self.index(50, -50, self.MAX_SPEED)
            self.middle(0, 0, self.MAX_SPEED)
            self.ring(-20, 20, self.MAX_SPEED)
            self.thumb(-12, -65, self.MAX_SPEED)

    def pinch(self):
        if self.side == 1: # Right Hand
            self.index(90, -90, self.MAX_SPEED)
            self.middle(90, -90, self.MAX_SPEED)
            self.ring(90, -90, self.MAX_SPEED)
            self.thumb(0, -75, self.MAX_SPEED)
        else: # Left Hand
            self.index(90, -90, self.MAX_SPEED)
            self.middle(90, -90, self.MAX_SPEED)
            self.ring(90, -90, self.MAX_SPEED)
            self.thumb(75, 5, self.MAX_SPEED)

    # --- Data Reading Methods ---
    
    def read_position(self, motor_id):
        """Reads the present position of a single motor in degrees."""
        pos_rad = self.controller.read_present_position(motor_id)
        
        # Handle different return types from rustypot
        if isinstance(pos_rad, (list, tuple)):
            if len(pos_rad) > 0:
                pos_rad = pos_rad[0]  # Take the first element if it's a list
            else:
                return 0.0  # Return 0 if empty list
        
        pos_deg = np.rad2deg(pos_rad)
        
        # Ensure we return a scalar value, not an array
        if isinstance(pos_deg, np.ndarray):
            return float(pos_deg.item())
        return float(pos_deg)

    def read_speed(self, motor_id):
        """Reads the present speed of a single motor."""
        speed = self.controller.read_present_speed(motor_id)
        
        # Handle different return types from rustypot
        if isinstance(speed, (list, tuple)):
            if len(speed) > 0:
                speed = speed[0]  # Take the first element if it's a list
            else:
                return 0.0  # Return 0 if empty list
        
        if isinstance(speed, np.ndarray):
            return float(speed.item())
        return float(speed)

    def read_load(self, motor_id):
        """Reads the present load of a single motor."""
        load = self.controller.read_present_load(motor_id)
        
        # Handle different return types from rustypot
        if isinstance(load, (list, tuple)):
            if len(load) > 0:
                load = load[0]  # Take the first element if it's a list
            else:
                return 0.0  # Return 0 if empty list
        
        if isinstance(load, np.ndarray):
            return float(load.item())
        return float(load)

    def read_voltage(self, motor_id):
        """Reads the present voltage of a single motor."""
        voltage = self.controller.read_present_voltage(motor_id)
        
        # Handle different return types from rustypot
        if isinstance(voltage, (list, tuple)):
            if len(voltage) > 0:
                voltage = voltage[0]  # Take the first element if it's a list
            else:
                return 0.0  # Return 0 if empty list
        
        if isinstance(voltage, np.ndarray):
            return float(voltage.item())
        return float(voltage)

    def read_temperature(self, motor_id):
        """Reads the present temperature of a single motor."""
        temp = self.controller.read_present_temperature(motor_id)
        
        # Handle different return types from rustypot
        if isinstance(temp, (list, tuple)):
            if len(temp) > 0:
                temp = temp[0]  # Take the first element if it's a list
            else:
                return 0.0  # Return 0 if empty list
        
        if isinstance(temp, np.ndarray):
            return float(temp.item())
        return float(temp)

    def get_all_motors_status(self):
        """
        Retrieves a complete status dictionary for all 8 motors.
        """
        status_list = []
        for i in range(1, 9):
            try:
                status = {
                    "id": i,
                    "position": round(self.read_position(i), 2),
                    "speed": self.read_speed(i),
                    "load": self.read_load(i),
                    "voltage": self.read_voltage(i),
                    "temperature": self.read_temperature(i),
                }
                status_list.append(status)
            except Exception as e:
                print(f"Could not read status for motor {i}: {e}")
                status_list.append({"id": i, "error": "read failed"})
        return status_list
