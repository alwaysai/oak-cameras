
"""
Use Oak camera object detection and centroid tracking.

Applications count uniques human faces in the frame in realtime.

To change the computer vision model, the engine and accelerator,
and add additional dependencies read this guide:
https://alwaysai.co/docs/application_development/configuration_and_packaging.html
Note: This application is designed to use models compiled for the usage with
Oak camera (Oak-1 & Oak-D)
"""
import time
import edgeiq
from edgeiq import oak


def face_enters(object_id, prediction):
    """Centroid tracker callback function.

    Function takes the object ID and ObjectDetectionPrediction
    as arguments. – A callback function to be called each time
    a new object is detected by the correlation tracker.
    """
    print("Face {} enters".format(object_id))


def face_exits(object_id, prediction):
    """Centroid tracker callback function.

    A callback function to be called each time an existing object is removed
    from the tracking list. This event occurs after the deregister frames count
    is exhausted which occurs after the object is last detected by the tracker.
    """
    print("Face {} exits".format(object_id))


def main():
    """Run object detector and centroid tracker."""
    tracker = edgeiq.CorrelationTracker(
            max_objects=5, enter_cb=face_enters, exit_cb=face_exits)

    fps = edgeiq.FPS()

    try:
        with edgeiq.oak.Oak('alwaysai/face_detection_0200_oak',
                        sensor=edgeiq.Sensor.res_1080,
                        video_mode=edgeiq.VideoMode.preview) as oak_camera, \
                        edgeiq.Streamer() as streamer:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection and tracking
            while True:
                frame = oak_camera.get_frame()
                results = oak_camera.get_model_result(confidence_level=.6)
                if results:
                    fps.update()
                    text = ["Faces Detected:"]

                    objects = tracker.update(results.predictions, frame)

                    # Update the label to reflect the object ID
                    predictions = []
                    for (object_id, prediction) in objects.items():
                        prediction.label = "face {}".format(object_id)
                        text.append("{}".format(prediction.label))
                        predictions.append(prediction)
                    text.append(("approx. FPS: {:.2f}".
                                format(fps.compute_fps())))
                    frame = edgeiq.markup_image(frame, predictions)
                streamer.send_data(frame, text)

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("Program Ending")


if __name__ == "__main__":
    main()
