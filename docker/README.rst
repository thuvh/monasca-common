======================================
Docker base image for Monasca services
======================================


List all labels on image (you need to have ``jq`` installed):

``docker inspect monasca-api:master | jq .[].Config.Labels``
