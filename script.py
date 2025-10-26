import cv2
import numpy as np
import serial
ser = serial.Serial('COM5', baudrate=9600)
ser.write(b'hello com')
A0 = 10000
def main():
    cap = cv2.VideoCapture(0)  # 0 for webcam
    fgbg = cv2.createBackgroundSubtractorMOG2(history=500, detectShadows=True, varThreshold=50)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        fgmask = fgbg.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        min_area = 500  # tune this

        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        if large_contours:
            dominant_contour = max(large_contours, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(dominant_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            M = cv2.moments(dominant_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            text = f"Area: {w*h} distance: {distance(w*h)} aim to: {direct(x,y,50*distance(w*h))}"
            ser.write(
                f"Area: {w * h} distance: {distance(w * h)} aim to: {direct(x, y, 50 * distance(w * h))}\n".encode())
            cv2.putText(frame, text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow("Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    ser.close()
    cap.release()
    cv2.destroyAllWindows()
def direct(x,y,r):
    return ((float(np.arctan(x/r))*180/3.1415)//1, (float(np.arctan(y/r))*180/3.1415)//1)
def distance(s):
    return np.sqrt(A0/s)
if __name__ == '__main__':
    main()

