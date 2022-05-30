# bap-intern
# Problem 1 - Table detection

Processing images, detecting edges and tables in images.

## Tasks
### Read & process image
* Read image from path
* Process image
  * Convert to grey
  * Blur image
  * Canny (if necessary)
  * AdaptiveThreshold
### Approach 1 (input 2, 4, 5, 6)
* Find contours
* Find all coordinates
* Crop original image into tables using found coordinates
* Detect horizontal & vertical lines in cropped image
* Compute number of sub-answers in a table.

### Approach 2 (input 3)
* Detecting horizontal & vertical lines in the original image
* Draw these lines on a blank image (bi)
* Find contours on (bi)
* Plot histogram and pick a threshold to define the gap between tables
* Crop original image into tables
* Divide a table into rows and compute number of cell in a row
* Number of sub-answers is sum of cells in a table.

## Installation

Clone the repo from Github and pull the project.
```bash
git clone https://github.com/namtp-ai/bap-intern.git
git checkout hanldn/problem1
git pull
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r requirements.txt
```

## Usage
Run approach 1
```bash
python problem1.py
```
Run approach 2
```bash
python problem1_input3.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
[Lê Hoàng Ngọc Hân - Đại học Bách Khoa - Đại học Đà Nẵng (DUT)](https://github.com/hanahh080601) 
