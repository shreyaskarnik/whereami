# WhereAMI

Predicting Geolocation from image using machine learning

## Background and Acknowledgements

This repo houses the code for predicting geolocation from a given image url in form of a restful API.

The model, pre-processing code and labels used in this project comes from [Multimedia Berkeley Group](https://github.com/multimedia-berkeley/tutorials) the model is a MxNet model trained on [YFCC100M Multimedia Commons](https://aws.amazon.com/public-datasets/multimedia-commons/) dataset.

Inspired from [@ranman](https://github.com/ranman)'s [Twitch livestream AI Twitter bot session](https://www.twitch.tv/videos/231561561)

This project was built to test the code locally, however if you follow the above interactive coding session you shoulw be able to deploy this on AWS easily.

## Usage

* Download the model using `python download.py`
* Execute `docker-compose up`

  * This will build the image based on the `Dockerfile` and start the API at `http://localhost:8080`
    * You can start testing the API using `cURL` or Postman
    ```bash
    curl -X POST \
    http://localhost:8080/invocations \
    -H 'Content-Type: application/json' \
    -d '{
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Statue_of_Liberty_7.jpg/250px-Statue_of_Liberty_7.jpg",
        "max_predictions": 5
        }'
    ```

  * You should see top 5 predictions returned in JSON array sorted by probability of the geolocation.
    ``` json
    [
        {
            "city": "New York City",
            "country": "US",
            "lat": "40.71427",
            "lon": "-74.00597",
            "region": "New York"
        },
        {
            "city": "New York City",
            "country": "US",
            "lat": "40.71427",
            "lon": "-74.00597",
            "region": "New York"
        },
        {
            "city": "New York City",
            "country": "US",
            "lat": "40.71427",
            "lon": "-74.00597",
            "region": "New York"
        },
        {
            "city": "New York City",
            "country": "US",
            "lat": "40.71427",
            "lon": "-74.00597",
            "region": "New York"
        },
        {
            "city": "New York City",
            "country": "US",
            "lat": "40.71427",
            "lon": "-74.00597",
            "region": "New York"
        }
    ]
    ```