# Distributed Object Detection on Edge Devices using tinyML
This repository contains the implementation of my mini-project for the 6th semester at Cochin University of Science and Technology. It is a part of my M.Sc. (Five Year Integrated) course in Computer Science, with a focus on Artificial Intelligence & Data Science.

The aim of this project is to reduce the load on the central server. This is achieved by performing inference on the edge device where data is collected, instead of sending it to the central server for inference. This approach can reduce server load, decrease latency, and enhance the inference rate.

The inference is performed on the edge device using the concept of TinyML.


## Use Case
- To corroborate the problem statement, the use case I am implementing is to detect whether a car has passed through any of the N number of cameras in a distributed mechanism.
- As per my problem statement, the detection of the cars and the comparison of the car’s similarity with the target image can be done on the edge device itself. The inferred data is then sent to the cloud for mapping the car’s journey.




## Architecture
![Overall Architecture](https://github.com/abdulhakkeempa/Distributed-Object-Detection/assets/92361680/b07135d7-c70a-4924-b60d-37feb06b81f4)

## Detailed Workflow
![Workflow](https://github.com/abdulhakkeempa/Distributed-Object-Detection/assets/92361680/dc8809b1-0184-4d2b-8cae-3edc826f47d3)
