import cv2 as cv
import numpy as np

from aif_edge_node.global_variables import GlobalVariables
from aif_edge_node.image_processing.image_detector.yolo_detector import YoloDetector
from aif_edge_node.image_processing.image_processor.image_processor import ImageProcessor

class OBBImageProcessor(ImageProcessor):
    def __init__(self):
        super().__init__()
        self.detector = YoloDetector(GlobalVariables.PROJECT_ROOT / 'checkpoints' / 'models' / 'obb' / 'olo11n-obb.pt')

    def _draw_bounding_boxes(self, image, bounding_boxes):
        """
        Draw (oriented bounding boxes on an image.

        Parameters:
            image (np.ndarray): The image/frame on which to draw.
            bounding_boxes (np.ndarray): Array of bounding boxes in the format [x, y, w, h, r].
        """
        for xywhr in bounding_boxes:
            x, y, w, h, r = xywhr

            # Prepare for cv2.boxPoints
            rect = ((x, y), (w, h), np.degrees(r))  # Convert angle to degrees
            box = cv.boxPoints(rect)  # Get the 4 vertices of the rotated rectangle
            box = np.int0(box)  # Convert vertex coordinates to integers

            # Draw the oriented bounding box
            cv.drawContours(image, [box], 0, (0, 0, 255), 2)  # Red color, thickness=2

        return image

    def _extract_bounding_boxes(self, inference_result) -> np.ndarray:
        return inference_result[0].obb.cpu().numpy().xywhr


