======================================
Docker base image for Monasca services
======================================


List all labels on image (you need to have ``jq`` installed):

``docker inspect monasca-api:master | jq .[].Config.Labels``

TODO(Dobroslaw): why pykafka and PyMySQL is needed
TODO(Dobroslaw): health check stuff
TODO(Dobroslaw): "instructions" for the child image (and refer to example folder...)
