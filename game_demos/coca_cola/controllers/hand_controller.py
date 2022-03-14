import threading
import cv2
import mediapipe as mp


class HandController(threading.Thread):

    def __init__(self, camera_index: int = 0, display_dim=(480, 420)):
        super().__init__()
        self.cap = cv2.VideoCapture(camera_index)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.is_running = True
        self.index_coordinates = [0, 0]
        self.display_dim = display_dim

    def stop(self):
        self.is_running = False

    def get_mapped_coordinates(self, moving_plane_size: tuple, offset: tuple):
        x = self.index_coordinates[0] * moving_plane_size[0] + offset[0]
        y = self.index_coordinates[0] * moving_plane_size[1] + offset[1]
        return x, y

    def run(self) -> None:
        with self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:
            while self.cap.isOpened() and self.is_running:
                ret, frame = self.cap.read()
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # Rendering results
                if results.multi_hand_landmarks:
                    for num, hand in enumerate(results.multi_hand_landmarks):
                        self.mp_drawing.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS,
                                                       self.mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2,
                                                                                   circle_radius=4),
                                                       self.mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                                   circle_radius=2),
                                                       )
                        self.index_coordinates[0] = hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                        self.index_coordinates[1] = hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                resized = cv2.resize(image, self.display_dim, interpolation=cv2.INTER_AREA)
                cv2.imshow('Hand Tracking', resized)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            self.cap.release()
            cv2.destroyAllWindows()
