#!/bin/bash

ssh l@192.168.122.252 "echo 123456 | sudo -S docker container prune"
sleep 1
ssh l@192.168.122.124 "echo 123456 | sudo -S docker container prune"
sleep 1
ssh l@192.168.122.219 "echo 123456 | sudo -S docker container prune"
sleep 1
ssh l@192.168.122.60 "echo 123456 | sudo -S docker container prune"
sleep 1
ssh l@192.168.122.7 "echo 123456 | sudo -S docker container prune"
sleep 1
ssh l@192.168.122.248 "echo 123456 | sudo -S docker container prune"