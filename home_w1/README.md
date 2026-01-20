## Question 1. Understanding Docker Images

Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What's the version of `pip` in the image?
~~~
docker run --rm -it python:3.13 bash
pip --version
~~~

