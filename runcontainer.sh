#!/bin/bash

docker run -t -p 13801:13800 --net=host --name="test_node" test_container
