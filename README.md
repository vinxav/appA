# App A

Create a network to be used by both containers (only once):

`docker network create crypto`

After running App B, run App A:

`docker run --network=crypto app-a `