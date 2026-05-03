## Base
You are a coding agent. Analyze the two codebases in the FNO folder and in Code/21cmFAST App. 
- FNO contains a test build of a Fourier Neural Operator network, which has been optimized to be used on this local machine. In the future, the plan is to scale up to proper computing hardware. 
- 21cmFAST App contains a front-and-backend implementation of a webapp doing simulations of the Epoch or Reionization, generating Lightcones for given z and ICs. These are saved in Code/21cmFAST App/data/outputs. 

## Goal
The immediate goals are as follows: 
- In the long run, the plan is using the FNO architecture to train on 21cmFAST ICs and Simulation Data to predict cosmological parameters for future z. 
- For that, first build a pipeline so that the data of the 21cmFAST simulations can be used with the FNO architecture. 
- Input parameters, for now, are the $\delta_{\text{matter}}(z)$, and the network will be trained to predict $x_{HI}(z)$. 

Instructions: 
- Find an efficient but flexible way to implement the pipeline for the data to feed into the network. 
- Document every step into a markdown file. That file should serve as a base for a documentation of the project. 

You can find additional project information in [[FNO Approach for 21cm Emulation]]. 