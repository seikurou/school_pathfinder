# school_pathfinder

## Usage:

Compatible with Python3.
Install required libraries: `pip install -r requirements.txt`

To run the program: `python main.py`

Example:
```
> python main.py
Welcome to the RBHS path finder
LIST OF LOCATIONS:
br   w2   408  901  s13
e1   w3   409  902  sw1
e2   w4   410  903  sw2
e3   w5   501  904  sw3
e4   w6   502  905  sw4
e5   w7   503  906  sw5
e6   w8   504  907  sw6
e7   201  505  908  sw7
e8   202  506  925  sw8
e9   203  601  asb  sw9
n1   204  602  e10  pool
n2   205  603  e11  kiosk
n3   206  604  e12  store
n4   301  605  e13  library
n5   302  606  e14  stadium
n6   303  607  e15  cafeteria
n7   304  608  e16  large quad
n8   305  609  gym  small quad
n9   306  610  lpr  lower field
s1   307  701  n10  north locker
s2   308  702  n11  south locker
s3   309  703  n12  boys bathroom
s4   401  704  n13  tennis courts
s5   402  801  n14  baseball field
s6   403  803  n15  girls bathroom
s7   404  804  n16  front of school
s8   405  805  s10  staff parking lot
s9   406  806  s11  student parking lot
w1   407  810  s12

The pathfinder will take a starting location on the RBHS campus and an ending location
and display an image showing the shortest path between the two locations. You need to
enter the locations so that it matches one of the supported locations listed above.

Which is the closest to your current location? (ex. E13, S1, 401, tennis courts)
  type here --> boys bathroom
Which is the closest to your destination?
  type here --> lower field
saved image as output/2020-09-01 20_35_30.png
```
Example output:
<img src="output/schoolModified 2019-03-29 20_53_32.png">
