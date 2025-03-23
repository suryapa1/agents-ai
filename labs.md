# Understanding AI Agents
## Session labs 
## Revision 1.1 - 03/23/25

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

Make sure to have started Ollama if you haven't.
```
ollama serve &
```
</br></br>
**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**Lab 1 - Creating a simple agent**

**Purpose: In this lab, we’ll learn about the basics of agents and see how tools are called.**

1. In our repository, we have a set of Python programs that we'll be building out to work with concepts in the labs. These are mostly in the *agents* subdirectory. Go to the *TERMINAL* tab in the bottom part of your codespace and change into that directory.
```
cd agents
```

2. For this lab, we have the outline of an agent in a file called *agent1.py* in that directory. You can take a look at the code either by clicking on [**agents/agent1.py**](./agents/agent1.py) or by entering the command below in the codespace's terminal.
```
code agent1.py
```

3. As you can see, this outlines the steps the agent will go through without all the code. When you are done looking at it, close the file by clicking on the "X" in the tab at the top of the file.

4. Now, let's fill in the code. To keep things simple and avoid formatting/typing frustration, we already have the code in another file that we can merge into this one. Run the command below in the terminal.
```
code -d ../extra/lab1-code.txt agent1.py
```

5. Once you have run the command, you'll have a side-by-side in your editor of the completed code and the agent1.py file.
  You can merge each section of code into the agent1.py file by hovering over the middle bar and clicking on the arrows pointing right. Go through each section, look at the code, and then click to merge the changes in, one at a time.

![Side-by-side merge](./images/aa5.png?raw=true "Side-by-side merge") 

6. When you have finished merging all the sections in, the files should show no differences. Save the changes simply by clicking on the "X" in the tab name.

![Merge complete](./images/aa6.png?raw=true "Merge complete") 

7. Now you can run your agent with the following command:

```
python agent1.py
```

8. You'll see some of the messages from the model loading. Then, eventually, you should see a section showing the call to the function, the return value from the function, and the final output from the run.

![Merge complete](./images/aa7.png?raw=true "Merge complete") 

9. Notice that the location *Paris, France* supplied in the user query was converted into an appropriate latitude and longitude for the tool call by the LLM. Then the output of the tool run was converted to a user-friendly weather report as the final answer.

10. (Optional) If you get done early and want to play around, you can try changing the user query. If you don't seem to get a response after the function is called, it may be due to the API limiting. Ctrl-C to cancel the run and try again.
<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 4 - Router Workflow with LangGraph Agent**

**Purpose: In this lab, we’ll see how to implement an agent in LangGraph that demos the router workflow.**

1. As we've done before, we'll build out the agent code with the diff/merge facility. Run the command below.
```
code -d ../extra/lab4-code.txt agent4.py
```

![Merge complete](./images/aa8.png?raw=true "Merge complete") 

2. In the *agent4.py* template, we have the imports and llm setup at the top filled in. Scroll to the bottom. At the bottom is the part to compile the workflow and example usage for three different use cases: a translation to French, a calculation, and a definition. The agent we build through LangGraph will look at each of these and route it to an appropriate node to handle it. This is the basis of the Agent Routing Workflow.

![Code to run agent](./images/aa9.png?raw=true "Code to run agent") 

3. Scroll back to the top, review each change and then merge each one in. When done, the files should show no differences. Click on the "X" in the tab at the top to save your changes to *agent4.py*.

![Merge complete](./images/aa10.png?raw=true "Merge complete") 

4. Now you can run the agent and see the results of each request being handled. There will be quite a bit of output so this may take a moment to run.

```
python lab4.py
```

![Execution](./images/aa11.png?raw=true "Execution") 

5. Now that we have our routing agent working, let's add one more enhancement. Since LangGraph is based on graphs, we can have it draw the nodes and edges of the graph so we can look at it on a web page. The updated code for this is in *extra/lab4-chart.txt*. We'll use the same merging process to add in code to draw a Mermaid chart and save the data in an html file. Run the command below, review the changes, then merge them in and close the diff to save. (Note there are two sets of changes - a line at the top and a larger section further down.)

```
code -d ../extra/lab4-chart.txt agent4.py
```

![Adding code for graph](./images/aa12.png?raw=true "Adding code for graph") 

6. After completing the merge and save, run the agent again. This time it should dump the graph information into a file named *index.html* in the same directory.

```
python agent4.py
```

![html generated](./images/aa13.png?raw=true "html generated") 

7. After this is completed, you can take a look at the graph by starting up a local server. Run the commands below in the terminal.

```
npm i -g http-server
http-server
```

8. After a moment, you should see a pop-up dialog that you can click on to open a browser to see the graph.

![opening graph on web](./images/aa14.png?raw=true "opening graph on web") 

9. This should then open up a web page showing the graph.

![visual graph](./images/aa15.png?raw=true "visual graph") 

10. When you're done looking at this, you can close the web page and then go back to the terminal and stop the *http-server* process with *Ctrl-C*.
    
<p align="center">
**[END OF LAB]**
</p>
</br></br>
 
