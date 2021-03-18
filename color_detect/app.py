"""
Use Oak camera object detectiong.

Applications attempts to determine the color of detected object by using
centroid pixel of its bounding box to determine the color of the object.

To change the computer vision model, the engine and accelerator,
and add additional dependencies read this guide:
https://alwaysai.co/docs/application_development/configuration_and_packaging.html
Note: This application is designed to use models compiled for the usage with
Oak camera (Oak-1 & Oak-D)
"""
import time
import edgeiq
import pandas as pd


# declaring global variables
r = g = b = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


def getColorName(R, G, B):
    """
    Get color name at centroid point of the bounding box.

    The function to calculate minimum distance from all colors and
    gets the most matching color for the point
    """
    minimum = 1000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


def main():
    """Run object detector."""
    fps = edgeiq.FPS()

    try:
        with edgeiq.Oak('alwaysai/ssd_v2_coco_oak') as oak_camera,\
                edgeiq.Streamer() as streamer:
            # Allow Oak camera to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = oak_camera.get_frame()
                results = oak_camera.get_model_result(confidence_level=.8)
                if results:
                    fps.update()

                    text = ["Oak Camera Detections:"]
                    text.append("approx. FPS: {:.2f}".
                                format(fps.compute_fps()))
                    text.append("Objects:")
                    for prediction in results.predictions:
                        center = tuple(int(round(val)) for val in
                                       prediction.box.center)
                        b, g, r = frame[center[1], center[0]]
                        cname = getColorName(r, g, b)
                        text.append("{}: {:2.2f}% color = {}".format(
                                    prediction.label,
                                    prediction.confidence * 100, cname))

                    # Mark up image for display
                    frame = edgeiq.markup_image(frame, results.predictions)

                streamer.send_data(frame, text)

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("Program Ending")


if __name__ == "__main__":
    main()
