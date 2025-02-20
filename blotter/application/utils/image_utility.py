import base64
import io

from PIL import Image
from mimetypes import guess_type

from utils.commons import Logger


class ImageUtility:

    @staticmethod
    def process_and_convert(image, quality=90) -> bytes:
        try:
            """
            Compress an image and convert it to binary format for database storage.

            Args:
                image (PIL.Image.Image or io.BytesIO): The image to process.
                quality (int): Compression quality (1-100).

            Returns:
                bytes: Binary data of the compressed image.
            """
            compressed_image = ImageUtility.loose_compression(image, quality=quality)
            binary_img = ImageUtility.convert_to_binary(compressed_image)
            return binary_img
        except Exception as e:
            Logger.get_logger().error(f"Error during image processing: {e}")

    @staticmethod
    def loose_compression(image_file, quality: int = 90):
        """
        Loosely compress an image with minimal quality loss.

        Args:
            input_path (str): Path to the input image.
            output_path (str): Path to save the loosely compressed image.
            quality (int): Compression quality (80-95 is recommended for loose compression).
        """
        image = Image.open(image_file)
        get_extension = ImageUtility.format_validation(image)
        # Ensure the image is in RGB mode
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        # Prepare a BytesIO buffer to store the compressed image
        compressed_image = io.BytesIO()
        ImageUtility.compression_type(compressed_image, get_extension, image, quality)
        compressed_image.seek(0)
        return compressed_image

    @staticmethod
    def compression_type(compressed_image, get_extension, image, quality):
        if get_extension == "PNG":
            # Compress PNG (quantize for smaller size)
            image = image.quantize(colors=256)  # Reduce colors
            image.save(compressed_image, format="PNG", optimize=True)
        else:  # Default to JPEG compression
            image.save(compressed_image, format="JPEG", optimize=True, quality=quality)
        return image


    @staticmethod
    def image_converter(image: io.BytesIO()):
        """This will convert image stored from database to base64 format to be rendered in the view."""
        if not image:
            raise ValueError('No image file uploaded.')

        try:
            image = ImageUtility.obj_to_byte(image)
            get_extension = ImageUtility.format_validation(image)
            result = None
            if image.mode == "RGBA" or get_extension == "PNG":
                result = ImageUtility.convert_to_base64_with_rgb_convertion(image)
            else:
                result = ImageUtility.convert_to_base64(image)
            return result
        except Exception as e:
            Logger.get_logger().error(f"Error during image conversion: {e}")

    @staticmethod
    def convert_to_base64(image):
        """
        Converts an image (memoryview, binary data, or PIL Image object) to a base64 string.
        The returned value can be used as a source for an image tag in HTML.
        Args:
            image: The input image. Can be a memoryview, bytes, or a PIL Image object.
        Returns:
            str: The base64-encoded string representation of the image.
        """
        try:
            if not isinstance(image, Image.Image):
                raise ValueError("The input is not a valid PIL Image object, memoryview, or binary data.")
            img_format = ImageUtility.format_validation(image)
            img_str = ImageUtility.base64_converter(image)
            return [
                f"data:image/{img_format.lower()};base64,{img_str}",
                img_format
            ]
        except Exception:
            """This will be returned because a fallback function will catch this and process it"""
            return image

    @staticmethod
    def format_validation(image):
        img_format = "JPEG"
        if image.format == "PNG":
            img_format = "PNG"
        if image.format == "JPG":
            img_format = "JPG"
        if image.format == "JPEG":
            img_format = "JPEG"
        return img_format

    @staticmethod
    def convert_to_base64_with_rgb_convertion(image):
        """
        NOTE: This function is specifically for images with RGBA mode.

        Converts an image (memoryview, binary data, or PIL Image object) to a base64 string.
        The returned value can be used as a source for an image tag in HTML.
        Args:
            image: The input image. Can be a memoryview, bytes, or a PIL Image object.
        Returns:
            str: The base64-encoded string representation of the image.
        """
        try:
            if not isinstance(image, Image.Image):
                raise ValueError("The input is not a valid PIL Image object, memoryview, or binary data.")
            img_format = ImageUtility.format_validation(image)
            if image.mode == "RGBA":
                image = image.convert("RGB")
            buffered = io.BytesIO()
            image.save(buffered, format=img_format)  # Save as JPEG
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            return [
                f"data:image/{img_format.lower()};base64,{img_str}",
                img_format
            ]
        except Exception:
            raise ValueError("Something went wrong while converting the image. Please contact support.")



    @staticmethod
    def base64_converter(image):
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str

    @staticmethod
    def obj_to_byte(image):
        if isinstance(image, memoryview):
            image = image.tobytes()

        if isinstance(image, (bytes, bytearray)):
            image = Image.open(io.BytesIO(image))
        return image

    @staticmethod
    def convert_to_image(image_data):
        if not image_data:
            raise ValueError('No image file uploaded.')

        # If the image data is a memoryview, convert it to bytes
        if isinstance(image_data, memoryview):
            image_data = image_data.tobytes()  # Convert memoryview to bytes

        # Now that image_data is bytes, open it using BytesIO
        image = Image.open(io.BytesIO(image_data))
        return image

    @staticmethod
    def convert_to_binary(image):
        if not image:
            raise ValueError('No image file uploaded.')
        return image.read()

    @staticmethod
    def image_size_validation(image):
        if image:
            if image.size > 10485760:
                raise ValueError('Image file too large. Size should not exceed 10MB.')

    @staticmethod
    def mime_type_validation(image):
        if not image:
            raise ValueError('No image file uploaded.')

        mime_type, _ = guess_type(image.name)
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']

        if mime_type not in allowed_types:
            raise ValueError('Invalid image file type. Only JPEG, JPG, and PNG files are allowed.')

    @staticmethod
    def compress_image(image):
        if not image:
            raise ValueError('Unable to compress files. No image file uploaded.')
        img = Image.open(image)
        img.save(image.path, quality=50, optimize=True)
        return image