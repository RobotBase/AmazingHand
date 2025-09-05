import time
import amazingctrl

# --- IMPORTANT ---
# Replace "/dev/tty.usbmodem5A7A0585381" with the actual port of your AmazingHand.
PORT = "/dev/tty.usbmodem5A7A0585381"

def monitor_motors(hand, duration=10):
    """
    Monitor all motor status for a specified duration.
    
    :param hand: AmazingHand instance
    :param duration: Monitoring duration in seconds
    """
    print(f"Monitoring motor status for {duration} seconds...")
    print("Format: Motor_ID | Position | Speed | Load | Voltage | Temperature")
    print("-" * 70)
    
    start_time = time.time()
    while time.time() - start_time < duration:
        status_list = hand.get_all_motors_status()
        
        # Print current timestamp
        elapsed = time.time() - start_time
        print(f"\nTime: {elapsed:.1f}s")
        
        for status in status_list:
            if 'error' not in status:
                print(f"Motor {status['id']:1d} | "
                      f"{status['position']:7.2f}° | "
                      f"{status['speed']:5.1f} | "
                      f"{status['load']:6.1f} | "
                      f"{status['voltage']:4.1f}V | "
                      f"{status['temperature']:3.1f}°C")
            else:
                print(f"Motor {status['id']:1d} | ERROR: {status['error']}")
        
        time.sleep(1)  # Update every second

def main():
    try:
        hand = amazingctrl.AmazingHand(port=PORT)
        hand.start()
        time.sleep(1)

        print("=== AmazingHand Real-time Sensor Monitoring ===\n")
        
        # Test 1: Monitor in open position
        print("Test 1: Monitoring in open position")
        hand.open()
        time.sleep(2)
        monitor_motors(hand, duration=5)
        
        # Test 2: Monitor during gesture changes
        print("\n\nTest 2: Monitoring during gesture sequence")
        gestures = [
            ("close", hand.close),
            ("point", hand.point),
            ("victory", hand.victory),
            ("ok", hand.ok),
            ("open", hand.open)
        ]
        
        for gesture_name, gesture_func in gestures:
            print(f"\nExecuting {gesture_name} gesture...")
            gesture_func()
            time.sleep(1)
            
            # Quick status check
            status = hand.get_all_motors_status()
            avg_load = sum(s.get('load', 0) for s in status) / len(status)
            print(f"Average motor load: {avg_load:.1f}")

        print("\n\nTest 3: Individual motor position reading")
        for motor_id in range(1, 9):
            try:
                pos = hand.read_position(motor_id)
                load = hand.read_load(motor_id)
                temp = hand.read_temperature(motor_id)
                print(f"Motor {motor_id}: Position={pos:.2f}°, Load={load:.1f}, Temp={temp:.1f}°C")
            except Exception as e:
                print(f"Motor {motor_id}: Error reading - {e}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

    finally:
        if 'hand' in locals():
            print("\nStopping the hand.")
            hand.stop()

if __name__ == '__main__':
    main()
