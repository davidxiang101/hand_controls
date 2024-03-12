import cv2
import numpy as np

def capture_video():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Step 2: Preprocess the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (35, 35), 0)

        # Step 3: Segment the hand
        # Thresholding to segment the hand. Adjust the threshold value as needed.
        _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

        # Step 4: Contour Detection
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Consider the largest contour as the hand
            hand_contour = max(contours, key=cv2.contourArea)

            # Step 5: Convex Hull and Defects
            hull = cv2.convexHull(hand_contour, returnPoints=False)
            defects = cv2.convexityDefects(hand_contour, hull)

            # Step 6: Gesture Recognition
            if defects is not None:
                # Count defects (spaces between fingers)
                finger_count = 0
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(hand_contour[s][0])
                    end = tuple(hand_contour[e][0])
                    far = tuple(hand_contour[f][0])

                    # Apply angle thresholding to count fingers
                    a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                    c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                    angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c)) * 57  # Convert to degrees

                    if angle <= 90:
                        finger_count += 1

                cv2.putText(frame, f'Fingers: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 2)

        cv2.imshow('Gesture', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    capture_video()
