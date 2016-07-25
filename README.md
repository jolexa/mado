# mado
mado is: Marathon Autoscaling Docker Oneshot, an attempt to autoscale your marathon apps
--------

## Vision
The vision is to have a Docker image that will run once to autoscale marathon applications.

I envision multiple backends that will be used. The actual scale up and down is a stable interface that should only change if upstream changes API spec.

Backend Support:

| Backend | Status | Environment Token Name |
| ----- | ----- | ----- |
| LogicMonitor | Supported | logicmonitor |
| AWS CloudWatch | Supported | cloudwatch |
| Others? | ??? | <nbsp> |

## Running
It should be very easy to run this wherever `marathon.mesos` resolves to the correct address (requires mesos-dns somewhere). Docker is used to provide a simple interface to run (though, it isn't too complicated if you choose to decompose it)

There are many environment variables in lieu of a config file or parameters to make this as re-usable as possible. They get passed to the Docker runtime. Backend specific variables have a common prefix and can be omitted it not used.

Common:

| Variable | Description |
| ------ | ------ |
| POLL_SERVICE | Supporting Services for polling. See key above for support |
| THRESHOLD | Threshold to take action |
| SCALE_UP_PERCENT | *(int)* Percentage to scale the MARATHON_APP_GROUP |
| SCALE_DOWN_PERCENT | *(int)* Percentage to scale the MARATHON_APP_GROUP |
| MARATHON_APP_GROUP | Group of apps to scale |

LogicMonitor:

| Variable | Description |
| ------ | ------ |
| LM_COMPANY | LogicMonitor Company |
| LM_USER | LogicMonitor User |
| LM_PASS | LogicMonitor Pass |
| LM_DATASOURCE | LogicMonitor Datasource |
| LM_DATAPOINT | LogicMonitor Datapoint |
| LM_HOST | LogicMonitor Host where datasource is applied |

CloudWatch:

| Variable | Description |
| ------ | ------ |
| CW_NAMESPACE | Namespace, allowed values [here](https://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/aws-namespaces.html) |
| CW_METRIC | Metric Name |
| CW_DIMENSION_NAME | Dimension Name |
| CW_DIMENSION_VALUE | Dimension Value |
| CW_AGGREGATION_TYPE | Aggregation Type, Supported: "Maximum" or "Average" |


## Contibutors and Contributions
See contributors

Standard, fork, PR, merge

Feedback welcome and desired!
