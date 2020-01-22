# UR5 with FIROS

## Usage
Check if the subscriptions have been created:
http://150.162.6.64:1026/v2/subscriptions/

If not, then run the shell script:

``` $ ./create_subs.sh ```

When created, you should see the following:
![guide](https://user-images.githubusercontent.com/24254286/72857932-dd62e780-3c9d-11ea-8cbd-189a775c1014.png)

Run FIROS:

``` $ roslaunch firos firos.launch ```

Run the skill/task from UR5 and the topic should be listened.


## Debug
If you don't see the data being showed in Grafana, the first thing to check is if the Orion Broker is receiving the data before transmitting it to the DBCrate:

``` $ curl 150.162.6.64:1026/v2/entities -s -S -H 'Accept: application/json' | python -mjson.tool ```

If this commands returns:

``` [] ```

Then the data is not being sent, meaning you should check the ``` /config ``` , i.e the ``` robots.json ``` and ``` config.json ``` files.

If it returns a whole message then the broker is receiving the messages correctly and the problem lies on the DBCrate-Grafana interface. Usually restarting the database does the thing.