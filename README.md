# Api_Rate_Limiter_Docker_image

This is a API rate limiter for each user/client by authenticating with a header. It is setup to 10 requests per second, 
It can be changed in the main/index.py
 
This uses a straight forward sliding window problem approach for ensuring that the 

Steps to build docker image and run:
1) Enter the location of the Extracted directory
2) Enter in terminal
   -> docker build -t ratelimiter .
  -> docker run –name ratelimiter -d -p 3000:5000  ratelimiter
3) Check if the server is running properly
  -> curl -X GET -H "X-API-KEY: VIADUCT-TEST" http://localhost:3000/limit
3) To kill the docker
  -> docker kill ratelimiter


