curl --request POST \
  --url 'http://150.162.6.64:1026/v2/subscriptions/' \
  --header 'content-type: application/json' \
  --data '{
  "description": "Pick-and-place robot changes",
  "subject": {
    "entities": [{"idPattern": ".*", "type": "pickandplace"}],
    "condition": { 
      "attrs": [ ]
    }
  },
  "notification": {
    "http": {
      "url": "http://quantumleap:8668/v2/notify"
    }
  }
}' 

curl --request POST \
  --url 'http://150.162.6.64:1026/v2/subscriptions/' \
  --header 'content-type: application/json' \
  --data '{
  "description": "3D Printer changes",
  "subject": {
    "entities": [{"idPattern": ".*", "type": "printer3d"}],
    "condition": { 
      "attrs": [ ]
    }
  },
  "notification": {
    "http": {
      "url": "http://quantumleap:8668/v2/notify"
    }
  }
}' 
