# trips-word-sense
A module that assigns word-sense probabilities to different TRIPS senses of a given word in a sentence. 

Follow these steps to install all the dependencies required:
1. `pip install supwsd` (A word sense disambiguation tool. Reference - http://www.aclweb.org/anthology/D17-2018)
2. `pip install pytrips` - https://github.com/mrmechko/pytrips
3. `pip install pyims` - (Another word sense disambiguation tool: https://pypi.org/project/pyims/)
4. Download two IMS zip files from - https://www.comp.nus.edu.sg/~nlp/software.html:
	<ul>
		<li>IMS - IMS_v0.9.2.1 </li>
		<li>IMS - Models (WordNet 3.0) </li>
	</ul>
5. Create a directory named **ims** and unzip and extract the contents of **IMS - IMS_v0.9.2.1** into it.
6. Put the unzipped model folder from 4. into the same directory **ims**
7. Run `sudo chmod 755 testPlain.bash` from terminal when in the **ims** directory

Now you are ready to run the code.
	
Check out the example notebook in code/Test_Examples.ipynb to see how to run any sentence using this system.  
The path of the **ims** directory is declared in the notebook.  
Please raise an issue if you find any bugs or errors.
