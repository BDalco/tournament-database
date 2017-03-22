Swiss-style tournament results database

Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament that has a database schema to store the game matches between players. Lastly, there is a Python module to rank the players and pair them up in matches in a tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

The following steps are required to run the application:

Setup Environment and run Test:

1. Install Vagrant and VirtualBox
	a. https://www.vagrantup.com/
	b. https://www.virtualbox.org/wiki/Downloads
2. Clone the tournament repository
	a. https://github.com/udacity/fullstack-nanodegree-vm
3. Launch the Vagrant VM and run the program
	a. To use the Vagrant virtual machine, navigate to the full-stack-nanodegree-vm/tournament directory in the terminal, then use the command vagrant up (powers on the virtual machine) followed by vagrant ssh (logs into the virtual machine).
	b. Remember, once you have executed the vagrant ssh command, you will want to cd /vagrant to change directory to the synced folders in order to work on your project, once your cd /vagrant, type cd /tournament to get to the tournament directory.
	c. From the commandline type 'psql' To build and access the database and then \i tournament.sql to import the tournament database.  Exit psql by typing \q
	d. Run the unit tests from the command line type 'python tournament_test.py'
