#Broken, Abandoned, and Forgotten Code

##Introduction

Check out http://shadow-file.blogspot.com for a  detailed series of articles on reverse engineering and exploiting Netgear SOHO routers.

This series of posts describes how abandoned, partially implemented functionality can be exploited to gain complete, persistent control of Netgear wireless routers.

In this series, I'll describe the process of specially crafting a malicious firmware image and a SOAP request in order to route around the many artifacts of incomplete implementation in order to gain persistent control of the router. I'll discuss reverse engineering the proper firmware header format, as well as the the improper one that will work with the broken code.


##What's this repository for?

Many of the installments in this series will feature code that aids in the various stages of reverse engineering and exploiting the target device. Each part of the series featuring new or updated code will have a corresponding folder here. If you clone this repo, you should be able to get the latest updates whenever a new part goes up on the blog just by doing a pull.

Check out [part 1](http://shadow-file.blogspot.com/2015/04/abandoned-part-01.html) here.

Note: you will require Bowcaster, which you can get [here](https://github.com/zcutlip/bowcaster).

