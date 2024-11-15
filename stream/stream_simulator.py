import time
import cv2 as cv
from .video import Video


class StreamSimulator:
    def __init__(self, vid_path):
        self.video = Video(vid_path)
        self.max_width = 1280 # TODO: make dynamic to suit input video
        self.max_height = 720
        self.target_fps = self.video.fps
        self.is_running = False
        self.display_width, self.display_height = self._calculate_display_dimensions()

    def start(self):
        self.is_running = True

        if not self.video.isOpened():
            raise IOError(f'Unable to open input video file. Path: {self.video.path}')

        self._play_video()

        self.stop()

    def _calculate_display_dimensions(self):
        display_width = self.video.width
        display_height = self.video.height

        if display_width > self.max_width or display_height > self.max_height:
            scale_ratio = min(self.max_width / display_width, self.max_height / display_height)
            display_width = int(display_width * scale_ratio)
            display_height = int(display_height * scale_ratio)

        return display_width, display_height

    def _play_video(self):
        target_frame_time = 1 / self.video.fps
        prev_frame_time = time.time()

        while self.is_running:
            iteration_start_time = time.time()

            ret, frame = self.video.read_frame()

            if not ret:
                print("End of video stream or error reading frame.")
                break

            frame = self._process_frame(frame)

            current_time = time.time()
            fps = int(1 / (current_time - prev_frame_time))
            prev_frame_time = current_time

            self._display_frame(frame, fps)

            # Exit if the 'q' key is pressed
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

            iteration_duration = time.time() - iteration_start_time  # time to process 1 frame
            self._enforce_target_frame_rate(target_frame_time, iteration_duration)

    def _enforce_target_frame_rate(self, target_frame_time, iteration_duration):
        wait_time = max(target_frame_time - iteration_duration, 0)
        time.sleep(wait_time)

    def _process_frame(self, frame):
        return cv.resize(frame, (self.display_width, self.display_height))

    def _display_frame(self, frame, fps):
        self._display_fps(frame, fps)

        cv.imshow('Video', frame)

    def _display_fps(self, frame, fps):
        # Overlay FPS text on the frame
        fps_text = f"FPS: {fps}"
        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        color = (255, 0, 0)  # Green color
        thickness = 2
        position = (10, 30)  # Top-left corner

        cv.putText(frame, fps_text, position, font, font_scale, color, thickness)

    def stop(self):
        """
        Stops the video stream, releases the video capture and destroys all openCV windows
        :return:
        """
        if not self.is_running:
            return

        self.is_running = False
        self.video.release()
        cv.destroyAllWindows()


