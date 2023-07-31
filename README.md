# TalkToArduino

This project was created to improve time-efficiency in geometry optimization calculations done through the SHARCNET computing network. On the server, dozens, if not nearly a hundred calculations would be submitted and be running at any given point. These calculations are completed in a 5 step process. Since SHARCNET does not provide an automated process for advancing submitted jobs from one step to the next, the submitter needs to do this manually. In order to prevent large time intervals between each step, submitters must frequently check the jobs' statuses on the server, which involves submitting a precise entry into a command-line interface. 

Using the integration of Python and Arduino, connected and loaded to an Arduino circuit board, this tedious task can be reduced into a solution where, by the press of pushbuttons on the circuit board, the pattern in which the lights are lit indicate the status of the jobs (i.e. in Queue, Running, or Done). If the jobs are done, it will display an on-going green light. If the jobs are running, the LED will blink quickly. If the jobs are in queue, the LED will blink slowly. 

Once the job status is indicated as "Done", submitters can then proceed to advance the jobs to the next step in the 5 step calculation process. 
