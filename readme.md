# Duohacker

This is a special tool crafted to hack the duo infinitely. Happy hacking

## Getting Started

Let's get started

### Prerequisities


In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

### Usage

#### Clone the repo

Open up your terminal and start cloning

```shell
git clone https://github.com/Logesh08/Duohacker.git
```

#### Building


Start building the image

```shell
cd Duohacker
docker build -t Duohacker .
```

#### Running

Run in docker

```shell
docker run Duohacker
```

Start the containers

```shell
docker compose up
```

#### Environment Variables

* `TOKEN` - Add your special token here
* `MAX_THREADS` - Maximum number of threads. Recommended value is 1 and Maximum value is 5
* `RANGE_SET` - It's restarts each thread after specific number of loops. Default value is 50
* `DB_REF` - Add your database reference here

## Built With

* Selenium v4.8.3
* Selenium Wire v5.1.0
* Python Decouple v3.8
* Firebase Admin v6.1.0

## Find Me

* [GitHub](https://github.com/Logesh08)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Logesh Krishna** - *Original work* 

See also the list of [contributors](https://github.com/your/repository/contributors) who 
participated in this project.

<!-- ## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details. -->