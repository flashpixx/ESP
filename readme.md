# ESP 8266 Project

## Configuration

Flash a file with the name ```config.json``` within the root directory and the following structure

```json
{
  "debug": false,
  "port": 3030,
  "ssid" : <Wifi SSID>,
  "password" : <Wifi Password>
}
```

## Run

```
telnet <ip> <port>
```