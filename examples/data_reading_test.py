import time
import amazingctrl
import json

# --- IMPORTANT ---
# Replace "/dev/tty.usbmodem5A7A0585381" with the actual port of your AmazingHand.
PORT = "/dev/tty.usbmodem5A7A0585381"

def print_status(status):
    """Helper function to print the status list in a readable format."""
    print(json.dumps(status, indent=2))

def main():
    try:
        hand = amazingctrl.AmazingHand(port=PORT)
        hand.start()
        time.sleep(1)

        print("--- Test 1: Reading status in a static 'open' position ---")
        hand.open()
        time.sleep(2) # Wait for the hand to settle
        static_status = hand.get_all_motors_status()
        print_status(static_status)
        time.sleep(2)

        print("\n--- Test 2: Reading status immediately after a 'close' action ---")
        hand.close()
        time.sleep(2) # Wait for the hand to close
        closed_status = hand.get_all_motors_status()
        print_status(closed_status)
        print("Note the 'load' values, they should be higher now.")
        time.sleep(2)
        
        print("\n--- Test 3: Continuous data reading during motion ---")
        print("The hand will slowly open while data is being read for 3 seconds.")
        hand.open() # Start the opening motion
        
        start_time = time.time()
        while time.time() - start_time < 3:
            dynamic_status = hand.get_all_motors_status()
            # To avoid flooding the console, we'll print a single line.
            # This line shows the position of the first two motors (index finger).
            pos1 = dynamic_status[0].get('position', 'N/A')
            pos2 = dynamic_status[1].get('position', 'N/A')
            load1 = dynamic_status[0].get('load', 'N/A')
            load2 = dynamic_status[1].get('load', 'N/A')
            
            print(f"Time: {time.time() - start_time:.1f}s | Index Finger Pos: ({pos1}, {pos2}) | Load: ({load1}, {load2})")
            time.sleep(0.2) # Read data 5 times per second

        print("\n--- Test 4: Testing additional gestures ---")
        print("Testing point gesture...")
        hand.point()
        time.sleep(2)
        
        print("Testing victory gesture...")
        hand.victory()
        time.sleep(2)
        
        print("Testing ok gesture...")
        hand.ok()
        time.sleep(2)
        
        print("Testing pinch gesture...")
        hand.pinch()
        time.sleep(2)
        
        print("Returning to open position...")
        hand.open()
        time.sleep(1)

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    finally:
        if 'hand' in locals():
            print("\nStopping the hand.")
            hand.stop()

if __name__ == '__main__':
    main()
