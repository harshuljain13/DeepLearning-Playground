#### Abstract

Several days back we found Dog Breed Identification challenge hosted by Kaggle. The goal was to build a model capable of doing breed classification of a dog by just looking into its image. We started thinking about possible approaches to build a model for doing this and what accuracy it might be able to achieve. Afer good research experiments, we found that transfer learning is a good way to build the robust model with good accuracy. Our model gives us around 85% accuracy.



#### Methodology

A dog's image is fed into Inception model. Inception model calculates the transfer values of the image using the pretrained weights. The output from Inception model i.e. transfer values goes through several fully connected (FC) layers. In our case there are 3 FC layers. the output of FC layers is fed finally to the softmax output probabilities of an image to belong to each class. Here each class is an separate breed. 

![Inception](http://localhost:8000/static/dogs_classification/images/inception_transfer_learning.png)

#### Training Results

```
Epoch:  19
Optimization batch:      1, Training Accuracy: 100.0%
Optimization batch:     11, Training Accuracy: 100.0%
Optimization batch:     21, Training Accuracy: 100.0%
Optimization batch:     31, Training Accuracy:  98.4%
Optimization batch:     41, Training Accuracy: 100.0%
Optimization batch:     51, Training Accuracy: 100.0%
Optimization batch:     61, Training Accuracy:  99.2%
Optimization batch:     71, Training Accuracy: 100.0%
Optimization batch:     81, Training Accuracy: 100.0%
Optimization batch:     91, Training Accuracy: 100.0%
Optimization batch:    101, Training Accuracy:  99.2%
Optimization batch:    111, Training Accuracy: 100.0%
Average accuracy for the Epoch:  99.7767857143
Epoch:  20
Optimization batch:      1, Training Accuracy: 100.0%
Optimization batch:     11, Training Accuracy: 100.0%
Optimization batch:     21, Training Accuracy: 100.0%
Optimization batch:     31, Training Accuracy: 100.0%
Optimization batch:     41, Training Accuracy: 100.0%
Optimization batch:     51, Training Accuracy: 100.0%
Optimization batch:     61, Training Accuracy: 100.0%
Optimization batch:     71, Training Accuracy: 100.0%
Optimization batch:     81, Training Accuracy: 100.0%
Optimization batch:     91, Training Accuracy: 100.0%
Optimization batch:    101, Training Accuracy:  99.2%
Optimization batch:    111, Training Accuracy: 100.0%
Average accuracy for the Epoch:  99.8046875
```

