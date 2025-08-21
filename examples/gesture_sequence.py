import time
import amazingctrl

# --- IMPORTANT ---
# Replace "/dev/tty.usbmodem5A7A0585381" with the actual port of your AmazingHand.
# On Windows, it might be "COM3", "COM4", etc.
# On Linux or Mac, it's typically "/dev/tty.usbmodemXXXX" or "/dev/ttyACM0".
PORT = "/dev/tty.usbmodem5A7A0585381"

def main():
    try:
        # 1. Initialize the hand controller
        # You can also specify side and calibration_data if needed, e.g.:
        # my_calibration = [3, 0, -5, -8, -2, 5, -12, 0]
        # hand = amazingctrl.AmazingHand(port=PORT, side=2, calibration_data=my_calibration)
        hand = amazingctrl.AmazingHand(port=PORT)

        # 2. Start the connection and enable motors
        hand.start()
        time.sleep(1) # Wait a moment for the hand to be ready

        # 3. Perform a sequence of gestures
        print("Performing gesture sequence...")

        print("Opening hand...")
        hand.open()
        time.sleep(2)

        print("Closing hand...")
        hand.close()
        time.sleep(2)

        print("Pointing...")
        hand.point()
        time.sleep(2)

        print("Victory sign...")
        hand.victory()
        time.sleep(2)

        print("OK sign...")
        hand.ok()
        time.sleep(2)

        print("Pinching...")
        hand.pinch()
        time.sleep(2)
        
        # Return to open position
        hand.open()
        time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check the serial port and ensure the hand is connected properly.")

    finally:
        # 4. Stop the hand and release the motors
        if 'hand' in locals():
            print("Stopping the hand.")
            hand.stop()

if __name__ == '__main__':
    main()
