# Network Visualization of Programming Languages

Created by following [Peter Gleeson's](https://medium.com/@petergleeson1) 2017 article,
[How to visualize the programming language influence graph](https://medium.com/free-code-camp/how-to-visualize-the-programming-language-influence-graph-7f1b765b44d1).

## Dependencies

-[ ] Python (3.8.2)
   -[ ] `pip3 install wikipedia`
-[ ] [Gephi](https://gephi.org/users/download/)
-[ ] [Sigma.js](http://sigmajs.org/)

## Run Graph Locally

The sigma file that was generated is in the `network` folder.

Run locally with a web server:

```commandline
python -m http.server
```

Then navigate to [http://0.0.0.0:8000/network/](http://0.0.0.0:8000/network/) in your browser.
