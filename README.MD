# 24i Bartender

This repository contains code for the 24i bartender (both pi & application). The `app` folder contains the React Native frontend app and the `pi` folder contains all code handling the actual hardware control.

## PI API

### /pumps

#### GET
Retrieves a list of all pumps and drinks attached to it.

*Response example*
```json
[
    {
        "id": 1,
        "drink": "vodka"
    },
    {
        "id": 2,
        "drink": "UNKNOWN"
    },
    {
        "id": 3,
        "drink": "UNKNOWN"
    },
    {
        "id": 4,
        "drink": "UNKNOWN"
    },
    {
        "id": 5,
        "drink": "UNKNOWN"
    },
    {
        "id": 6,
        "drink": "UNKNOWN"
    },
]
```

#### PUT
Allows to attach a drink to a pump.

*Request body example*
```json
{
    "id": 2,
    "drink": "gin"
}
```

*Response 400 error example*
```json
{
    "message": "This pump can not be set"
}
```

*Response 200 example*
```json
{
    "message": "Pump updated"
}
```

### /recipes

#### GET
Retrieves a list of recipes available on the server

*Response 200 example*
```json
[
    {
        "id": 1,
        "name": "moscow mule"
    }
]
```

#### POST

*Request body example*
```json
{
    "name": "gin tonic",
    "parts": [
        {
            "drink": "gin",
            "percentage": 50
        },
        {
            "drink": "tonic",
            "percentageg": 50
        }
    ]
}
```

*Response 200 example*
```json
{
    "message": "Recipe created"
}
```

### /pour

#### POST
Starts pouring a given drink

*Request body example*
```json
{
    "parts": [
        {
            "drink": "gin",
            "percentage": 50
        },
        {
            "drink": "tonic",
            "percentageg": 50
        }
    ]
}

```

*Response 400 example*
```json
{
    "message": "Non compatible drink"
}
```

*Response 200 example*
```json
{
    "message": "Drink pour started"
}
```

## Raspberry PI pinout

### Pump Pins
|Pin|Description|
|---|-----------|
|17|Pump 1|
|27|Pump 2|
|22|Pump 3|
|23|Pump 4|
|24|Pump 5|
|25|Pump 6|

### LED Pins
|Pin|Description|
|---|-----------|
|16|Red|
|20|Green|
|21|Blue|