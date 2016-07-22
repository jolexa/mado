# mado
mado is: Marathon Autoscaling Docker Oneshot, an attempt to autoscale your marathon apps
--------

## Vision
The vision is to have a Docker image that will run once to austoscale marathon applications.

I envision multiple (pluggable) backends that will be used. The actual scale up and down is a stable interface that should only change if upstream changes API spec.

## Running
It should be very east to run this wherever `marathon.mesos` resolves to the correct address (requires mesos-dns somewhere). Docker is used to provide a simple interface to run (though, it isn't too complicated if you choose to decompose it)

Environment Variables:

| Variable | Description |
| ------ | ------ |
| Fill me out | . |
| . | . |

## Contibutors and Contributions
See contributors

Standard, fork, PR, merge

Feedback welcome and desired!
