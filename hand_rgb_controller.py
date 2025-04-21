import cv2
import mediapipe as mp
import serial
import time

# === Setup ===
arduino = serial.Serial('COM5', 9600)
time.sleep(3) # let the arduino breathe

mp_hands_module = mp.solutions.hands
hand_detector = mp_hands_module.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils

camera = cv2.VideoCapture(0)

last_rgb_sent_time = 0
send_cooldown = 0.2

# === Main Loop ===
while camera.isOpened():
    frame_exists, video_frame = camera.read()
    if not frame_exists:
        break

    video_frame = cv2.flip(video_frame, 1)
    frame_height, frame_width, _ = video_frame.shape

    # Define interactive zones
    zone_width, zone_height = 400, 300
    red_zone_coords = (0, 0, zone_width, zone_height)
    green_zone_coords = (frame_width // 2 - zone_width // 2, 0, frame_width // 2 + zone_width // 2, zone_height)
    blue_zone_coords = (frame_width - zone_width, 0, frame_width, zone_height)

    # Draw zones on screen
    cv2.rectangle(video_frame, red_zone_coords[:2], red_zone_coords[2:], (0, 0, 255), -1)
    cv2.rectangle(video_frame, green_zone_coords[:2], green_zone_coords[2:], (0, 255, 0), -1)
    cv2.rectangle(video_frame, blue_zone_coords[:2], blue_zone_coords[2:], (255, 0, 0), -1)

    # Add labels to zones
    cv2.putText(video_frame, 'RED', (50, zone_height // 2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
    cv2.putText(video_frame, 'GREEN', (frame_width // 2 - 90, zone_height // 2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
    cv2.putText(video_frame, 'BLUE', (frame_width - zone_width + 50, zone_height // 2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

    # === Hand detection ===
    rgb_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)
    detection_result = hand_detector.process(rgb_frame)

    red_value, green_value, blue_value = 0, 0, 0  # Reset RGB each frame

    if detection_result.multi_hand_landmarks:
        detected_hand = detection_result.multi_hand_landmarks[0]
        fingertip_landmark = detected_hand.landmark[8]
        fingertip_x = int(fingertip_landmark.x * frame_width)
        fingertip_y = int(fingertip_landmark.y * frame_height)

        # Detect which zone the finger is in
        if red_zone_coords[0] <= fingertip_x <= red_zone_coords[2] and red_zone_coords[1] <= fingertip_y <= red_zone_coords[3]:
            red_value = 255
            print("Red zone")
        elif green_zone_coords[0] <= fingertip_x <= green_zone_coords[2] and green_zone_coords[1] <= fingertip_y <= green_zone_coords[3]:
            green_value = 255
            print("Green zone")
        elif blue_zone_coords[0] <= fingertip_x <= blue_zone_coords[2] and blue_zone_coords[1] <= fingertip_y <= blue_zone_coords[3]:
            blue_value = 255
            print("Blue zone")

        # Send RGB to Arduino if cooldown passed
        current_time = time.time()
        if current_time - last_rgb_sent_time > send_cooldown:
            arduino.write(bytes([red_value, green_value, blue_value]))
            last_rgb_sent_time = current_time

        # Draw hand landmarks
        drawing_utils.draw_landmarks(
            video_frame, detected_hand, mp_hands_module.HAND_CONNECTIONS,
            drawing_utils.DrawingSpec(color=(0, 0, 255), thickness=3, circle_radius=4),
            drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=2)
        )

    # Show current RGB values
    cv2.putText(video_frame, f"RGB: ({red_value}, {green_value}, {blue_value})", (frame_width // 2 - 150, frame_height - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display final frame
    cv2.imshow("Hand RGB Control", video_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
camera.release()
cv2.destroyAllWindows()
arduino.close()
