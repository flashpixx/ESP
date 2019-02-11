# ESP 8266 Project

## Configuration

Flash a file with the name ```config.json``` within the root directory and the following structure

```json
{
  "debug": false,
  "accesspoint": false,
  "hostname": <hostname>,
  "ssid" : <Wifi SSID>,
  "password" : <Wifi Password>,
  "threaded": true,
  "port": 80,
  "www": "/www"
}
```

## Micro-Webserver

Using [Micro-Webserver](https://github.com/jczic/MicroWebSrv) for a REST-API
