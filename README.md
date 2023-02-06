# Priority Places Explorer

The [Priority Places Explorer](https://priorityplaces.cdrc.ac.uk/) is a tool developed by the [CDRC](https://www.cdrc.ac.uk/) in partnership with [Which?](https://www.which.co.uk/) for visual analysis of the [Priority Places for Food Index](https://data.cdrc.ac.uk/dataset/priority-places-food-index/) to help identify local areas who are most at risk of food insecurity in the context of increases in the cost of living. 


## Attribution

The Priority Places Explorer tool is developed by 

- [Peter Baudains](https://github.com/peterbaudains/)
- [Francesca Pontin](https://github.com/FrancescaPontin/)

With support from:

- Emily Ennis
- Michelle Morris
- Robyn Naisbitt
- The team at [Which?](https://www.which.com/)

The Priority Places for Food Index has been developed by the Consumer Data Research Centre at the University of Leeds in collaboration with Which?. Data used in the development of the index is released under [Open Government License v3](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). We also acknowledge data provided by the Consumer Data Research Centre, an ESRC Data Investment ES/L011840/1; ES/L011891/1. [Internet User Classification](https://data.cdrc.ac.uk/dataset/internet-user-classification) data by Alexiou, A. and Singleton, A. (2018) contains Ofcom data (2016) and CDRC data from Data Partners (2017). We also acknowledge the [E-Food Desert Index](https://data.cdrc.ac.uk/dataset/e-food-desert-index/), developed by Newing and Videira (2020).

## License

This visualisation tool is released under a permissive MIT license, permitting the use, distribution and modification of the tool. This allows organisations to develop their own versions of the tool, for example with internal datasets visualised on top of the Priority Places for Food Index. If you do use this tool for internal purposes and to inform decision-making of some kind, then please let us know at info@cdrc.ac.uk.

## Setup (with Docker)

To setup this application with Docker you will need a local copy of this repository (the example below uses the [GitHub CLI](https://cli.github.com/)) and [Docker installed](https://docs.docker.com/get-docker/).

To build a Docker image using the provided Dockerfile, you use the [`docker build`](https://docs.docker.com/engine/reference/commandline/build/) command via a terminal application with a Docker-enabled user.

```bash
# using GitHub CLI clone the repository locally
$ gh repo clone Leeds-CDRC/priority-places-explorer

# enter the repository
$ cd priority-places-explorer

# build the docker image using the provided Dockerfile with the below tag
$ docker build . -t priority-places-explorer:latest
```

This will build the Docker image locally (you can view all local images with the `docker images` command). 

You can create a running instance of the Docker image by using the [`docker run`](https://docs.docker.com/engine/reference/run/) command:

```bash
# run the specified docker image
# forwarding port 8000 from within the container to the host machine
$ docker run -p 8000:8000 priority-places-explorer:latest
```

The application should then be accessible via http://localhost:8000/