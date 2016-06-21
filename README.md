# lsdserver
[![Build Status](https://travis-ci.org/GeoffWilliams/lsdserver.svg?branch=master)](https://travis-ci.org/GeoffWilliams/lsdserver)

## Linked Sensor Data Server

### Work In Progress -- not working yet!
Please get in touch if interested in contributing

[API -- UNSTABLE!](api.md)
[SQLAlchemy backend](backend_sqlalchemy.md)


### What does this do right now?
...Basically nothing.  I've wanted to work on this project but never get chance and there's always a bunch of things I need to do before I can work on this.

That said, I do now have (partial) Dockerfile to at least boot the flask application.  This needs to be improved to use docker compose to gain database support, etc.

Still, here's a cool screenshot of the main page just to prove this still even runs!
![main_screen](images/main_screen.png)

### What is this supposed to be?
A REST web service and GUI for viewing and managing [Linked Data](https://en.wikipedia.org/wiki/Linked_data) - A powerful concept for modelling data relationships that's been built into the web since day 1.

The idea is to provide a quick and easy way to apply these concepts to [Time Series Data](https://en.wikipedia.org/wiki/Time_series) so that useful data can be delivered with minimal complexity.  The idea is to hook this up to a half finished DIY weather station I built with an Arduino...
