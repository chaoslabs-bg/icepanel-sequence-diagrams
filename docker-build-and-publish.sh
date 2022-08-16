#!/bin/bash

docker build -f Dockerfile -t cladmin/icepanel_mermaid_sequence:v1 .
#docker tag cladmin/icepanel_mermaid_sequence:v1 docker.io/cladmin/icepanel_mermaid_sequence:latest
#docker push cladmin/icepanel_mermaid_sequence:v1