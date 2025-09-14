
The Quine-McCluskey algorithm is a systematic method for simplifying Boolean functions that works for any number of variables. This program:

· Accepts input minterms
· Converts them to binary form
· Uses the Quine-McCluskey table to find prime implicants (PIs)
· Identifies essential prime implicants (EPIs) using the Petrick method
· Generates the final simplified Boolean function

How It Works

1. Receives variables and input minterms from the user
2. Converts minterms to binary form
3. Constructs the Quine-McCluskey table and finds prime implicants
4. Creates a coverage table to identify EPIs
5. Finds essential prime implicants using the Petrick method
6. Generates the final simplified Boolean function

Limitations

· The program may slow down with a large number of minterms
· Only supports SOP (Sum of Products) form
