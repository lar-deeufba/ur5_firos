# Configuration-Files

FIROS needs 3 different configuration files inside the Configuration-Folder. An example Configuration-Folder can be
found in the `config`-Folder at the base of this repository. It needs to contain the files `config.json`, `robots.json`
and `whitelist.json` (optionally: `robotdescriptions.json`).

In the follwing each of the configuration files are explained in detail:

---

## `config.json`

The `config.json`-Configuration contains all basic FIROS-Configuration-Parameters which can be manipulated by the user.
No parameters are required, but you should specify it anyway, since you need to give FIROS Parameters, so that it can
publish and subscribe on that.

Inside this file you can specify multiple configurations. Via the `"environment"`-attribute you can select a specific
configuration as shown in the following example:

```json
{
    "environment": "test",

    "test": {
        "context_type": "MyRobotContextType",
        "server": {
            "port": 10100
        },
        "contextbroker": {
            "address": "192.168.0.97",
            "port": 1026,
            "subscription": {
                "throttling": "0",
                "subscription_length": 300,
                "subscription_refresh_delay": 0.9
            }
        },
        "log_level": "INFO",
        "interface": "enp1234"
    }
}
```

We also added here the contextbroker configuration, since we want to publish and subscribe data onto it.

Here is the list of all currently possibilities for a configuration:

| Attribute              | Value                                                                                                                                                                                                                                                              | Required |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------: |
| "interface"            | Can be `"public"` or another string of one of the interfaces given by `ip link` or by `ifconfig`. If set to `"public"`, the public IP-address is set for the Map-Server (via [this](http://ip.42.pl/raw)). Otherwise the (specified) interface IP-address is used. |    x     |
| "log_level"            | Can be either `"INFO"` (Default), `"DEBUG"`, `"WARNING"`, `"ERROR"` or `"CRITICAL"`.                                                                                                                                                                               |          |
| "node_name"            | This sets the ROS-Node-Name for this FIROS instance. The default is `"firos"`.                                                                                                                                                                                     |          |
| "ros_subscriber_queue" | The queue-size of the `rospy.Publisher`. See more [here](http://wiki.ros.org/rospy/Overview/Publishers%20and%20Subscribers). Default is `10`                                                                                                                       |          |
| "context_type"         | This sets the context type of an entity (the `type`-value of the base-entity). Default is `"ROBOT"` but can be changed if necessary                                                                                                                                |          |
| "rosbridge_port"       | Changes the ROS-Port, where to listen. Default is `9090`                                                                                                                                                                                                           |          |
| "server"               | An object `{}` which contains the attribute `"port"`                                                                                                                                                                                                               |          |
| "contextbroker"        | An object `{}` which contains the attributes `"adress"`, `"port"` and `"subscriptions"`                                                                                                                                                                            |    x     |
| "pub_frequency"        | An Integer of Milliseconds. This limits the number of publishes e.g. to the Context-Broker. This blocks the next publish for `pub_frequency` milliseconds.                                                                                                         |          |

### `"server"`-Configuration

The server configuration only has one attribute `"port"` which is defaulting to `10100`. You can change the port if you
experience errors. This usually occurs when this port is already occupied by another application.

### `"contextbroker"`-Configuration

The contextbroker configuration need to specifiy the `"address"` and `"port"` attribute to point to a running
Context-Broker. If you are running a local Context-Broker, `"address"` can also be set to `"localhost"`.
`"subscriptions"`-value is again another object `{}` which can contain the following:

| Attribute                    | Value                                                                                                                                                                                                                                                                                |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "throttling"                 | The throttling value as specified [here](https://fiware-orion.readthedocs.io/en/master/user/ngsiv2_implementation_notes/index.html#notification-throttling). Default is set to `0`.                                                                                                  |
| "subscription_length"        | The subscription length on the Context-Broker in seconds. Default is `300`. This only sets the [subscription length `expires` attribute](https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv2/index.html#subscriptions).                                             |
| "subscription_refresh_delay" | Depending on the subscription length, this value tells FIROS when to refresh a subscription. Default is set to `0.9` and cannot be larger than `1` or lower than `0`. It refreshes automatically the subscription in `"subscription_length" * "subscription_refresh_delay"` seconds. |

---

## `robots.json`

This configuration describes which information the FIROS-instance should publish to the Non-ROS-World and publish into
the ROS-World. There exist two different point of views: so we decided, that the publish-subscribe-terminology is at the
Non-ROS-World (e.g. Context-Brokers) point of view. Here is an example to publish `turtlesim`'s message/topic
`Pose`-information into the Non-ROS-World by subscribing to it. Accordingly, if the Non-ROS-World somehow receives any
Information about the `cmd_vel` (`Twist`-Information), its data is published into the ROS-World:

```json
{
    "turtle1": {
        "topics": {
            "cmd_vel": {
                "msg": "geometry_msgs.msg.Twist",
                "type": "publisher"
            },
            "pose": {
                "msg": "turtlesim.msg.Pose",
                "type": "subscriber"
            }
        }
    }
}
```

This json in particular listens to the rostopic `/turtle1/pose` with the message type `"turtlesim.msg.Pose"` (the
corresponding python message from `turtlesim/Pose`) and sends all retreived data to the specified server in the
Non-ROS-World. It publishes data into `/turtle1/cmd_vel` after receiving a notifcation of the server from the
Non-ROS-World from type `geometry_msgs/Twist`.

To clarify this behaviour, please have a look at this example with the Non-ROS-World being an Orion Context-Broker :

![Illustration](../media/pubsub-Illustration.png)

The green arrows are specified by the `config.json` (and `whitelist.json`). The corresponding black arrows are derived
from the green arrows, which happens automatically.

You do not have to specify `publisher` and `subscriber` of all available topics or at all for a robot. Only specify the
needed ones, which need to be displayed from/or need to obtain information on the Non-ROS-World

```json
{
    "ROBOT_ID": {
        "topics": {
            "TOPIC_1": {
                "msg": "PYTHON_REPRESENTATION_MESSAGE_TYPE",
                "type": "publisher"
            },
            "TOPIC_2": {
                "msg": "PYTHON_REPRESENTATION_MESSAGE_TYPE",
                "type": "subscriber"
            }
        }
    },
    "ROBOT_ID_2": {
        "topics": {
            "TOPIC_1": {
                "msg": "PYTHON_REPRESENTATION_MESSAGE_TYPE",
                "type": "subscriber"
            }
        }
    }
}
```

The Information given by the `robots.json` is appended/replaced to the `whitelist.json` which is described below.

---

## `whitelist.json`

As the name suggests, the `whitelist.json` functions as a whitelist to let FIROS know which messages it should keep
track of. Given an environment where already ROS-Applications are running, FIROS will automatically subscribe to all
available topics if no `whitelist.json` is given. In a small ROS-World with few ROS-Applications, this can be desirable.
But this can cause problems in a ROS-World, where many ROS-Applications are running. To let FIROS only subscribe to
specific topics, the following configuration can be used:

```json
{
    "turtle2": {
        "publisher": ["cmd_vel"],
        "subscriber": ["pose"]
    }
}
```

This only allows FIROS to subscribe/publish to `"/turtle2/pose"` and `"turtle2/cmd_vel"` plus the extra-configuration
given in `robots.json` which in the above example would also be `"/turtle1/pose"` and `"turtle1/cmd_vel"`.

**Note**, that an empty configuration of `whitelist.json` (`-> {}`) will also behave as an
non-existent-configuration-file. Usually for normal usecases, the `whitelist.json` contains the same information as the
`robots.json` and should be sufficient.

**Note:** The FIROS only captures running ROS-Applications at the startup. All applications started after FIROS will not
be recognized.

**Note:** The `whitelist.json` does not need to know the actual Message-Type. FIROS automatically looks up the
Message-Type. However, the "Message-Implementation" still needs to be present locally at the FIROS-Instance (via the
`msgs`-Folder, or compiled by catkin)

The `whitelist.json` also supports Regular Expressions (Regex), so you can refer to more Robots and Topics in just a few
lines.

Here we address all `turtle[a-zA-Z0-9]+` and `robot[a-zA-Z0-9]+` Robots with their topics:

```json
{
    "turtle\\w+": {
        "publisher": ["cmd_vel"],
        "subscriber": ["pose"]
    },
    "robot\\w+": {
        "publisher": ["cmd_vel.*teleop", ".*move_base/goal", ".*move_base/cancel"],
        "subscriber": [".*move_base/result"]
    }
}
```

---

## `robotdescriptions.json`

This configuration is optional and just appends additional information into the Non-ROS-World if even implemented.

E. g. The Context-Broker puts them under the `"descriptions"`-attribute. Those can be Links/Strings or maybe some
'static' values you need to have present for a robot/topic.

It can look like this:

```json
{
    "turtle1": {
        "descriptions": [
            "http://wiki.ros.org/ROS/Tutorials/UsingRxconsoleRoslaunch",
            "http://wiki.ros.org/ROS/Tutorials/UnderstandingNodes"
        ]
    }
}
```

Or like this:

```json
{
    "turtle1": {
        "descriptions": {
            "MySanatiyValue": 42,
            "SomeReferenceLink": "http://wiki.ros.org/ROS/Tutorials/UnderstandingNodes"
        }
    }
}
```
