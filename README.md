
<h1><b> Python PathFinder </b></h1>


<h3>Prerequisites</h3>
<h5><ul>
<li>The file files.txt must be in the same directory as the code.</li>
<li>The file files.txt must contain a list of graph file names, one per line.</li></ul></h5>
<h3>Introduction</h3>
<h5><ol>
<li>Execute the code.</li>
<li>Select the desired graph file name by entering the corresponding number.</li>
<li>Enter the desired number of random distance tests.</li>
<li>Enter the desired time tolerance for the test to fail to yield results in seconds.</li></ol></h5>
The code will then perform N-tests on two random points using 5 different types of algorithms. The results of the tests will be appended to an Excel spreadsheet (.xlsx).


<h5>Observation:<p>Both .gr and .co must have the same name before the extension format</p></h5>

<h5>Example:<p>graph.gr and graph.co</p></h5>

<h3>Python Dependencies</h3>
<ul>
<li>openpyxl</li>
<li>psutil</li>
</ul>

<h4>To install the dependencies, run the following command:</h4>

```bash
pip install openpyxl psutil
```

<h3>Running the code</h3>

```bash
python main.py
```

<h3>All graphs were taken from:</h3>
<a href="http://www.diag.uniroma1.it/~challenge9/download.shtml">diag.uniroma1.it</a>