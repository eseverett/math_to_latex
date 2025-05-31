import cv2
import numpy as np

class ImageProcessing:

    def __init__(self, image: np.ndarray) -> None:
        self.input_image     = image

        self.gaussian_kernal = 5
        self.gaussian_sigma  = 1

        self.threshold_color = 255
        self.block_size      = 15
        self.constant        = 2

        self.target_h = 64

        self.processed_image = None

    def run_preprocessing(self) -> None:
        """
        1) Convert to grayscale
        2) Apply Gaussian blur
        3) Adaptive threshold (inverted)
        4) Find largest contour, crop, compute angle from that contour
        5) Rotate the cropped patch by the angle
        6) Resize to fixed height
        """

        # 1) Grayscale
        gray = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)

        # 2) Gaussian blur
        blurred = cv2.GaussianBlur(
            gray,
            (self.gaussian_kernal, self.gaussian_kernal),
            self.gaussian_sigma
        )

        # 3) Adaptive threshold (white ink on black)
        binary = cv2.adaptiveThreshold(
            blurred,
            self.threshold_color,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            self.block_size,
            self.constant
        )

        # 4) Find contours, crop to largest
        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cropped = binary[y:y+h, x:x+w]

            # Compute angle from the full-image contour
            rect = cv2.minAreaRect(largest_contour)
            angle = rect[-1]

            # Rotate the cropped patch
            h_crop, w_crop = cropped.shape[:2]
            center = (w_crop // 2, h_crop // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            adjusted = cv2.warpAffine(
                cropped,
                M,
                (w_crop, h_crop),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
        else:
            adjusted = binary

        # 6) Resize to fixed height (self.target_h), maintain aspect ratio
        h0, w0 = adjusted.shape
        if h0 == 0 or w0 == 0:
            output = np.zeros((self.target_h, self.target_h), dtype=np.uint8)
        else:
            scale = self.target_h / float(h0)
            new_w = int(w0 * scale)
            output = cv2.resize(
                adjusted,
                (new_w, self.target_h),
                interpolation=cv2.INTER_AREA
            )

        self.processed_image = output

    def get_processed_image(self) -> np.ndarray:
        """
        Returns the processed image after preprocessing.
        """

        if self.processed_image is None:
            raise ValueError("Processed image is not available. Please run preprocessing first.")
        return self.processed_image
