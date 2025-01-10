# Pruner.js Study

## Overview

This repository contains the code used in the study investigating the effectiveness of [Pruner.js](https://github.com/overbrowsing/pruner), a JavaScript library designed to optimise responsive images through viewport-based rendering. The study evaluates Pruner.js’ performance, its ability to reduce server-side footprints, and its approach to addressing what we term pixel waste—image areas extending beyond the visible aperture—compared to HTML5.1 methods picture element and srcset attribute.

For detailed results and analysis, please refer to the published study [here](link-to-published-study).

## How to Repeat the Study

### Prerequisites

- Node.js installed on your machine.
- Python installed on your machine.

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/overbrowsing/pruner-study
    cd pruner-study
    ```

2. **Install Dependencies**:
    ```bash
    npm install
    pip install -r requirements.txt
    ```

4. **Run the Python Scripts**:

    #### Get Flickr Images
    [**get-flickr.py**](dataset/get-flickr.py): Downloads images from NASA's [Flickr Commons](https://www.flickr.com/commons) account based on specified criteria. Follow the prompts to create a CSV file and download images.
    ```bash
    cd dataset
    ```
    Make sure to add the `api-key.json` file to the dataset folder. The file should contain your Flickr API key in the following format:
    ```json
    {
    "api_key": "YOUR_KEY_HERE"
    }
    ```
    Then run:
    ```bash
    python get-flickr.py
    ```

    #### Process Images

    [**process-images.py**](implementation/process-images.py): Processes the downloaded images, resizing and cropping them for different methods. This will create folders and HTML files for each method.
    ```bash
    cd ../implementation
    python process-images.py
    ```

    #### Calculate Results

    [**calc-results.py**](implementation/calc-results.py): Calculates the results of the image processing, including file sizes and number of requests. This will generate a CSV file with the results and display a bar chart.
    ```bash
    python calc-results.py
    ```

    #### Calculate Pixel Waste

    [**calc-waste.py**](waste/calc-waste.py): Calculates the pixel waste for different viewport sizes. This will print the pixel waste percentages for different models.
    ```bash
    cd ../pixel\ waste
    python calc-waste.py
    ```

    #### Select Average Size Pages
    
    [**select-pages.py**](performance/select-pages.py): Selects the mean size project from the processed images and prepares it for evaluation. This will copy the selected project to a new folder for sharing on GitHub Pages.
    ```bash
    cd ../performance
    python select-pages.py
    ```

## Contributing

Contributions are welcome. Please feel free to [submit an issue](https://github.com/overbrowsing/pruner-study/issues) or a [pull request](https://github.com/overbrowsing/pruner-study/pulls).

## License

pruner-study is released under the [MIT](/LICENSE) license. Feel free to use and modify it as needed.