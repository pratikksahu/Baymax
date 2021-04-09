## Baymax
Personal Assistant on Wheels

## Table of contents
- [Tech/framework used](#Tech/framework-used)
- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
   - [Windows](#Windows)
      - Setting Up Virtual Environment(#Setting-Up-Virtual-Environment)

## Tech/framework used
<b>Built With</b>
* [Signup PageKite](http://pagekite.net/)
* [Alexa Custom Skill](https://developer.amazon.com/en-US/alexa)

## Prerequisites
- Python 3.x

## Installation
### Windows
*  Setting Up Virtual Environment <b>[Optional]</b>
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
* <b>Install required dependencies</b>
   ```
   pip install -r req.txt  
   ```
* <b>Get face recognition model and label encoder </b>
   - [Pretrained Model](https://github.com/pratikksahu/walle/tree/recognizer)
   - [Train Yourself](https://github.com/pratikksahu/walle/tree/train_model)
   - Copy "classifier" to .\walle\

* <b>Run</b>
   ```
   python pagekite.py 5000 "your pagekite endpoint"
   python alexa.py
   ```
   
   
