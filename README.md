
<h1><b> Python PathFinder </b></h1>

**Instructions**

<h5>
<ol>
<li>To use the code, first make sure that the file `files.txt` is in the same directory as the code. The file `files.txt` should contain a list of the graph file names, one per line.</li><br>

<li>Once the code is running, it will prompt you to select a graph file name. Enter the number of the graph file name that you want to use.</li><br>

<li>Next, the code will prompt you to enter the number of random distance tests that you want to make. Enter the number of tests that you want to make.</li><br>

<li>Finally, the code will prompt you to enter the time tolerance for the test to fail to yield results. Enter the time tolerance in seconds.</li><br>
</ol></h5>
The code will then start making the random distance tests. The results of the tests will be added to a .xlsx.


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