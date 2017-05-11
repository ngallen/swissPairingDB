TO intialize the databse use command:
psql tournament_test.sql

*This require Postgresql to be installed

To run the testing script use command:
python tournament_test.sql

All functions called by the testing script are located in:
tournament.py

If the script executes correctly the prompt should print:
"""
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!
"""
