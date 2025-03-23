# Understanding AI Agents
## Session labs 
## Revision 1.0 - 03/23/25

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

2. For this lab, we have the outline of an agent in a file called *agent1.py* in that directory. You can take a look at the code either by clicking on [**agents/agent1.py**](./genai/nn.py) or by entering the command below in the codespace's terminal.
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

9. Notice that the location *London* supplied in the user query was converted into an appropriate latitude and longitude for the tool call by the LLM. Then the output of the tool run was converted to a user-friendly weather report as the final answer.

10. (Optional) If you get done early and want to play around, you can try changing the user query.
<p align="center">
**[END OF LAB]**
</p>
</br></br>

 
