import time
import amazingctrl

# --- IMPORTANT ---
# Replace "/dev/tty.usbmodem5A7A0585381" with the actual port of your AmazingHand.
PORT = "/dev/tty.usbmodem5A7A0585381"

def main():
    try:
        hand = amazingctrl.AmazingHand(port=PORT)
        hand.start()
        time.sleep(1)

        print("Demonstrating single finger control with the Index finger.")

        # Start from an open hand position
        print("1. Opening hand to start.")
        hand.open()
        time.sleep(2)

        # Control the index finger independently
        print("2. Bending the index finger.")
        # hand.index(angle_1, angle_2, speed)
        # angle_1: Controls side-to-side movement
        # angle_2: Controls forward/backward bending
        hand.index(90, -90, hand.CLOSE_SPEED)
        time.sleep(2)

        print("3. Straightening the index finger.")
        hand.index(-40, 40, hand.MAX_SPEED)
        time.sleep(2)

        print("4. Wagging the index finger side-to-side.")
        hand.index(-10, 80, hand.MAX_SPEED)
        time.sleep(0.5)
        hand.index(-80, 10, hand.MAX_SPEED)
        time.sleep(0.5)
        hand.index(-10, 80, hand.MAX_SPEED)
        time.sleep(0.5)
        hand.index(-80, 10, hand.MAX_SPEED)
        time.sleep(0.5)

        # Return to open position
        print("5. Returning to open hand position.")
        hand.open()
        time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'hand' in locals():
            print("Stopping the hand.")
            hand.stop()

if __name__ == '__main__':
    main()
