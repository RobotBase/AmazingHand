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
