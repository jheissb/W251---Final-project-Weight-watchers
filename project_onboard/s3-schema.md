# S3 Schema

## S3 Hierarchy
wait-watcher-bucket/  
* face-id/  
    * d-1/  
        * x011,x022..... (binary face image)  
    * id-2/  
        * x011,x022..... (binary face image)  
* user-historical-data/  
    * id-1/year/month/day/
        * user object json 

## User Object Json Schema
```
{
    "bmi" : 23.01,
    "wait-height-ratio" : 0.45,
    "face" : x011,x022..... (binary face image), 
    "body" : x011,x022..... (binary body image),
    "timestamp" : 2020-12-04 12:34:908Z 
}
```