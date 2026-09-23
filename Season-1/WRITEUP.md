# Secure Code Game — Season 1:. Foundations

I completed the five Season 1 challenges in my GitHub Codespace, using AI assistance to review the code, implement fixes, and verify the results. The exercises showed why passing ordinary functional tests does not necessarily mean an application is secure.

In Level 2, Matrix, the C program checked the upper limit of a settings index but allowed negative values. An attacker could write before the settings array and change the account's administrator flag. I fixed this by checking both index boundaries before accessing memory, validating numeric conversions, and rejecting nonexistent users. I also. corrected the account counter so each account receives one valid identifier. The exploit now leaves the user unprivileged.

In Level 3, Social Network, file paths could escape the intended directory. Checking whether input starts with “..” was insufficient because a path could begin with “./” instead. I resolved paths, including symbolic links, and checked their common directory before opening files. Both profile pictures and tax forms now reject paths outside the permitted directory.

In Level 4, Data Bank, user input was inserted directly into SQL, allowing additional commands to modify data. I replaced executable query strings with fixed SQL statements and bound parameters. The old arbitrary-query interfaces now accept only narrowly defined stock lookups. I corrected one upstream exploit assertion to check that malicious input returns no rows and leaves stock data unchanged.

The other fixes addressed payment precision and weak password, salt, token, and secret handling. All functional tests, active exploit checks, and added security checks passed in Codespaces. These exercises reinforced the importance of validating inputs and separating untrusted data from executable instructions.
