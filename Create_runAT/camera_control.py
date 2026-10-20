from pypylon import pylon
import matplotlib.pyplot as plt
import numpy as np
from Create_runAT import get_product


# Define a reaction named 'camera' to trigered when the barcode reader is used and activate the camera


def camera(base_URL, token, list_productID):
    """
    This function activate the camera when the atttribute barcode_use in Arksuite is True.

    Parameters:
    - base_URL (str): The server url.
    - token (str): token to be able to log int the server
    - list_productID (list):

    Returns:
    -
    """
    camera_on = False
    authentification_needded = False

    for i in list_productID:

        use_barcode = get_product.use_barcode(base_URL, token, i)

        if use_barcode == "authentification error":
            authentification_needded = True
            break
        else:
            while use_barcode is True:

                use_barcode = get_product.use_barcode(base_URL, token, i)

                camera_on = True

                print("the vial with product ID" + str(i) + " is moving")
                """
                        camera = pylon.InstantCamera(
                            pylon.TlFactory.GetInstance().CreateFirstDevice()
                        )
                        camera.Open()

                        numberOfImagesToGrab = 100
                        camera.StartGrabbingMax(numberOfImagesToGrab)

                        camera.ExposureTime.Value = camera.ExposureTime.Min

                        while camera.IsGrabbing():
                            grabResult = camera.RetrieveResult(
                                5000, pylon.TimeoutHandling_ThrowException
                            )

                            if grabResult.GrabSucceeded():
                                # Access the image data.
                                print("SizeX: ", grabResult.Width)
                                print("SizeY: ", grabResult.Height)
                                img = grabResult.Array
                                print("Gray value of first pixel: ", img[0, 0])

                            grabResult.Release()
                        camera.Close()
                        """

    return camera_on, authentification_needded
