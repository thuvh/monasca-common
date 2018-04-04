====================
Docker example image
====================

Example image to show how to build child containers from `monasca-base` image.

Use health check functionality to provide information for Docker if service
running inside container is healthy. Avoid using `curl` directly and instead
use `health_check.py` written with specific service in mind. It will provide
more flexibility like when creating JSON request body.


| Variable                  | Default                 | Description                                        |
|-------------------------- |-------------------------|----------------------------------------------------|
| `STAY_ALIVE_ON_FAILURE`   | `false`                        | If true, container runs 2 hours after tests fail   |
