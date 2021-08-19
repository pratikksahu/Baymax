## Baymax
Personal Assistant on Wheels


## WEB UI


https://user-images.githubusercontent.com/58379829/130020254-9703ce2b-c5f4-40ac-a48f-77a857207900.mp4

## Model


https://user-images.githubusercontent.com/58379829/130029498-d17a01a2-f075-48ac-87f7-6d071d18d407.mp4




## Table of contents
- [Tech/framework used](#Tech/framework-used)
- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
   - [Windows](#Windows)
      - [Setting Up Virtual Environment](#Setting-Up-Virtual-Environment) <b>Optional</b>
      - [Install required dependencies](#Install-required-dependencies)
      - [Get Trained model](#Get-face-recognition-model-and-label-encoder)
      - [Run](#Run)

## Tech/framework used
<b>Built With</b>
* [Signup PageKite](http://pagekite.net/)
* [Alexa Custom Skill](https://developer.amazon.com/en-US/alexa)

## Prerequisites
- [Python 3.9.1](https://www.python.org/downloads/release/python-391/) <b>Not tested above 3.9.1 </b>

## Installation
### Windows
*  ### Setting Up Virtual Environment
   *  <b>Install Virtual Env package </b>
       ```
       py -m pip install --user virtualenv
       ```
   *  <b>Initialize Virtual Env </b>   
      *  Create Virutal Env 
         ```
         py -m venv "environment name"
         ```
      *  Activate Virtual Env 
         ```
         .\"environment name"\Scripts\activate
         ```
      *  Add env folder to .gitignore if using git
* ### Install required dependencies
   ```
   pip install -r req.txt  
   ```
* ### Get face recognition model and label encoder
   - [Pretrained Model](https://github.com/pratikksahu/walle/tree/recognizer)
   - [Train Yourself](https://github.com/pratikksahu/walle/tree/train_model)
   - Copy "classifier" to .\walle\

* ### Run
   ```
   python pagekite.py 5000 "your pagekite endpoint"
   python alexa.py
   ```
   
   
