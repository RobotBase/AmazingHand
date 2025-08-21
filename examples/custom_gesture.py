import time
import amazingctrl

# --- IMPORTANT ---
# Replace "/dev/tty.usbmodem5A7A0585381" with the actual port of your AmazingHand.
PORT = "/dev/tty.usbmodem5A7A0585381"

def create_thumbs_up(hand):
    """
    Creates a custom 'Thumbs Up' gesture by controlling individual fingers.
    This function is an example of how to build your own gestures.
    """
    print("Creating a custom 'Thumbs Up' gesture...")
    
    # 1. Curl the index, middle, and ring fingers into a fist
    hand.index(90, -90, hand.CLOSE_SPEED)
    time.sleep(0.1) # Small delay between finger movements
    hand.middle(90, -90, hand.CLOSE_SPEED)
    time.sleep(0.1)
    hand.ring(90, -90, hand.CLOSE_SPEED)
    time.sleep(0.1)
    
    # 2. Position the thumb upwards.
    #    The exact angles might need tuning for your specific hand calibration.
    hand.thumb(0, -75, hand.MAX_SPEED)

def main():
    try:
        hand = amazingctrl.AmazingHand(port=PORT)
        hand.start()
        time.sleep(1)

        # Start from an open hand position
        print("1. Opening hand to start.")
        hand.open()
        time.sleep(2)

        # Execute the custom gesture
        print("2. Executing custom gesture.")
        create_thumbs_up(hand)
        time.sleep(3) # Hold the gesture

        # Return to open position
        print("3. Returning to open hand position.")
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
