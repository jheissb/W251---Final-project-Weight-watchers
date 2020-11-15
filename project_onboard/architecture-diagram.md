#Arhitecture Diagram
![diagram](archtecture-digram.png)


Sample message in 
imagedetection/bodyextractor
imagedetection/faceextractor
```
{
    capturedTimestamp: "",
    id: "12345" use code generated from face (hashing etc),
    imageBlob: "x011..."
}
```

Sample message in 
imagedetection/bodyprocessor
imagedetection/faceprocessor
```
{
    capturedTimestamp: "",
    id: "12345" use code generated from face (hashing etc),
    imageBlob: "x011...",
    processedImageBlob: "...",
    faceMetadta: {},
    bodyMetadta: {},
    BMI: 21
}
```
