# oak-cameras-repo

![1b7194b7c4a79d3c471d3645b0d0a2c8_original](https://user-images.githubusercontent.com/21957723/111654915-6b653000-87c6-11eb-9e5b-b6525eba000c.png)


The Oak-1 and Oak-D cameras have built-in chips for artificial intelligence, eliminating the security, latency and cost issues found in cloud based inferencing. The cameras can determine where objects are located in the space around them, as well as their trajectory, in real time. The cameras feature built-in Intel Myriad X chips for running the machine learning inferencing locally.  This Repo shows you how to use these amazing cameras with the alwaysAI platform providing powerful easy to use option for them to create commercial products.


The Oak camera hardware (both models) includes a 12-megapixel auto-focus camera sensor with a wide horizontal field of view up to 4056 x 3040 resolution. The raw video output is at up to 4K/60fps with hardware 4K H.265 video encoding.  The Oak-D in addition to the main camera sensor that both models share provides spatial AI leveraging stereo depth.   


Use cases for Oak cameras are:
1. Navigation     - How to move a robot or drone around obstacles
2. Agriculture    - Whether produce is ripe for picking
3. Safety         - Monitoring worksites for safety violations and accidents


The alwaysAI API’s support support object detection, classification, pose estimation and spatial AI capabilities of the devices.

## Repo Programs
| Folder                     	| Description                                                                                              	|
|----------------------------	|----------------------------------------------------------------------------------------------------------	|
| basics           	          | Program demonstrate how to start the camera, capture images and inference those images. Application use object detection to detect human faces and centroid tracker to provide a unique face count |            
| color_detect            	  | Program use object detection and the centroid pixel of the object's bounding box to do color estimation of the that detected object|
## Running
The Oak Camera can be connected to either USB 3 or USB 2 hub, If use USB 2 make sure you adjust the API to indicate its usage for applications to work (defaults for the API is USB 3)

Use the alwaysAI CLI to build and start these applications:

Configure: `aai app configure`

Build: `aai app install`

Run: `aai app start`


## Support
Docs: https://alwaysai.co/docs/edgeiq_api/index.html

Oak Camera Docs: https://alwaysai.co/docs/edgeiq_api/oak.html

Community Discord: https://discord.com/invite/z3t9pea

Email: contact@alwaysai.co
