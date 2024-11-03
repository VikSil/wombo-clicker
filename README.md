# Wombo clicker

This script automates A.I. image generation on [Wombo Dream](https://dream.ai/create) website. 

It takes in prompts from *.csv* files located in `words/01_new_prompts`. Each line in an input file must have three columns, separated by pipe:
* prompt text
* image style
* number of iterations

**Example**:

    racoon birthday|pastel_v3|5

will generate five images of racoon birthday in pastel style.

**Available styles are**:

* dreamland_v3
* cartoon_v3
* surrealism_v3
* expressionism_v3
* impressionism_v3
* pastel_v3
* diorama_v3
* papercut_v3
* flat_v3
* graffiti_v3

If no style is given, a random style will be chosen for each iterartion at runtime.

You can put as many input files in the new promts folder as you like, they will be processed in a loop. Generally speaking, many small prompt files will yield less failures than a few large files.

## Dockerisation

Docker image of this repo is available [here](https://hub.docker.com/repository/docker/viksil/wombo-clicker/general).

In order to dockerise the code from scratch, run the following command:

    docker build . -t wombo-clicker --no-cache


## Running the script

In desktop environment, run the `main.py` file that is located in the `scripts` folder, either via GUI or in CLI:

    python ./scripts/main.py

In order to run the Docker image from bash terminal, use the command:

    docker run -v "/$(pwd)/pics:/wombo_clicker/pics" -v "/$(pwd)/words:/wombo_clicker/words" -it wombo-clicker


It will take a minute for the script to initialise. It will start by outputting a message `I am a clicker` to console, followed by the prompts it has read from the input folder. While running, the script will output information about each prompt it is processing.

Generated images will be downloaded into `pics/010_new` folder.

The execution of the script can be a hit-or-miss. Sometimes the Wombo website gets stuck and never outputs the image. There are some pop-ups that cannot be closed. In such cases processing of the remaining prompts in file will fail, and the script will output error messages to console. All failed prompts will be put into a new file to reprocess again. Generally speaking, many small prompt files are better than a few large files. If you are behind a VPN, it can help to switch server if the script repeatedly fails to perform. 

Processed files will be moved to either `words/02_processed` folder (if all lines were processed sucessfully) or `words/03_failed` folder (if some of the lines failed). 

The `main.py` script runs in an infinite loop checking for new files in `words/01_new_prompts` folder every 60 seconds, until the container or program is shut down.