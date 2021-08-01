import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture('pose1.mp4')


def angle_calc(a,b,c):
    a = np.array(a) #shoulder to elbow
    b = np.array(b) #elbow
    c = np.array(c) #elbow to shoulder

    radians = np.arctan2(c[1]-b[1], c[0]- b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                    #distance formula
    #  y-coordinates             c[1] = y2 b[1] = y1 ,
    #  x-coordinates             c[0] = x2  b[0] = x1
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle


with mp_pose.Pose(min_detection_confidence = 0.7, min_tracking_confidence = 0.7) as pose:
    # counter = 0
    # stage = None


    while cap.isOpened():
        ret, frame = cap.read()
        # rendor stuff
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # make detection
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # extract landmarks

        try:
            landmarks = results.pose_landmarks.landmark

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            #angle Calculation
            ang = angle_calc(shoulder, elbow, wrist)
            angle = round(ang, 2)

            #rendor on screen
            cv2.putText(image, "Angle of flex: " + str(angle), tuple(np.multiply(elbow, [1140, 780]).astype(int)),
                        cv2.FONT_HERSHEY_PLAIN, 2.5, (255, 255, 255), 2, cv2.LINE_AA)

            #logic


        except:
            pass

        cv2.rectangle(image,  (0,0), (455,193), (255, 128, 0), -1)
        cv2.putText(image, "Status Bar", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2,
                        cv2.LINE_AA)
        if angle > 165:
            cv2.putText(image, "Legal Delivery", (0, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2,
                        cv2.LINE_AA)
        if angle < 15:
            cv2.putText(image, "Illegal Delivery", (0, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2,
                        cv2.LINE_AA)




        # showing detection
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)


        cv2.imshow("Input Window", image)

        if cv2.waitKey(5) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()