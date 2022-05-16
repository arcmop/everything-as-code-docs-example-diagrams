## How to build 

1. Build docker for multi OS
   ```sh
    #Prepare docker image
    $ cd docker
    $ docker build -t diagrams:v1 .
    $ cd ..
    ```   
2. Run container passing filename
   ```sh
   #It will create a filename called: ocp_dev_cluster.png
   $ docker run --rm -v $PWD:/diagrams -w /diagrams diagrams:v1 diagram.py
   ```
