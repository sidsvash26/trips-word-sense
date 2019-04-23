# trips-word-sense
A module that assigns word-sense probabilities to different TRIPS senses of a given word in a sentence. Word-senses can be predicted using IMS or SupWSD. 

Follow these steps to install all the dependencies required:
1. `pip install supwsd` (A word sense disambiguation tool. Reference - http://www.aclweb.org/anthology/D17-2018)
2. `pip install pytrips` - https://github.com/mrmechko/pytrips
3. `pip install pyims` - (Another word sense disambiguation tool: https://pypi.org/project/pyims/)
4. Run `bash get_models.sh` to download IMS models and software. This will create an ims directory in the root directory of the project.
5. You'll need a SupWSD API key to run their Python API. You can get it by registering here: https://supwsd.net/supwsd/register.jsp 

Now you are ready to run the code.  
	
Check out the example notebook in code/Demo_notebook.ipynb to see how to run any sentence using this system.  

The path of the **ims** directory is declared in the notebook.    

Please raise an issue if you find any bugs or errors.  
