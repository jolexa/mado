# mado
mado is: Marathon Autoscaling Docker Oneshot, an attempt to autoscale your marathon apps
--------

## Vision
The vision is to have a Docker image that will run once to autoscale marathon applications.

I envision multiple (pluggable) backends that will be used. The actual scale up and down is a stable interface that should only change if upstream changes API spec.

## Running
It should be very east to run this wherever `marathon.mesos` resolves to the correct address (requires mesos-dns somewhere). Docker is used to provide a simple interface to run (though, it isn't too complicated if you choose to decompose it)

There are many environment variables in lieu of a config file or parameters to make this as re-usable as possible. They get passed to the Docker runtime. Backend specific variables have a common prefix and can be omitted it not used.

| Variable | Description |
| ------ | ------ |
| POLL_SERVICE | Supporting Services for polling. Allowed: 'logicmonitor' |
| LM_COMPANY | LogicMonitor Company |
| LM_USER | LogicMonitor User |
| LM_PASS | LogicMonitor Pass |
| LM_DATASOURCE | LogicMonitor Datasource |
| LM_DATAPOINT | LogicMonitor Datapoint |
| LM_HOST | LogicMonitor Host where datasource is applied |
| THRESHOLD | Threshold to take action |
| SCALE_UP_PERCENT | *(int)* Percentage to scale the MARATHON_APP_GROUP |
| SCALE_DOWN_PERCENT | *(int)* Percentage to scale the MARATHON_APP_GROUP |
| MARATHON_APP_GROUP | Group of apps to scale |

## Contibutors and Contributions
See contributors

Standard, fork, PR, merge

Feedback welcome and desired!
