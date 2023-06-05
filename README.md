# SantaChallenge

This project in relation to the FTP_Alg module of the Master of Science in Engineering (https://www.msengineering.ch/). The challenge is based on the santas stolen sleigh challenge on kaggle (https://www.kaggle.com/c/santas-stolen-sleigh). The aim is to find the most efficient way for santa to load his sleigh and deliver the christmas gifts over the world. The list of gifts are found in data/gifts.csv and using the jupyter-notebook in verification/santa-Visualize_and_verify.ipynb the submission can be visualized. 

The main approach in this solution was to pack first the heaviest gifts and fill the sleight with other gifts in the area. Afterwards we tried to optimize the created routes. The performance of our submission was quite poor. Other teams used greedy approach like e.g. nearest neighbour heuristic method and achieved better results.
