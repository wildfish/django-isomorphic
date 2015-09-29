Running: `siege -b -c 10 -t10S http://localhost:8000/`


# Plain Django template

    Transactions:		        1606 hits
    Availability:		      100.00 %
    Elapsed time:		        9.64 secs
    Data transferred:	        0.87 MB
    Response time:		        0.06 secs
    Transaction rate:	      166.60 trans/sec
    Throughput:		        0.09 MB/sec
    Concurrency:		        9.94
    Successful transactions:        1606
    Failed transactions:	           0
    Longest transaction:	        0.15
    Shortest transaction:	        0.03

# Django isomorphic template



    Transactions:		        1710 hits
    Availability:		      100.00 %
    Elapsed time:		        9.01 secs
    Data transferred:	        0.93 MB
    Response time:		        0.05 secs
    Transaction rate:	      189.79 trans/sec
    Throughput:		        0.10 MB/sec
    Concurrency:		        9.93
    Successful transactions:        1710
    Failed transactions:	           0
    Longest transaction:	        0.10
    Shortest transaction:	        0.02
    
    
    
    
    
Running: `siege -b -c 10 -t30S http://localhost:8000/`

# Plain Django template

    Transactions:		        5047 hits
    Availability:		      100.00 %
    Elapsed time:		       29.29 secs
    Data transferred:	        2.75 MB
    Response time:		        0.06 secs
    Transaction rate:	      172.31 trans/sec
    Throughput:		        0.09 MB/sec
    Concurrency:		        9.98
    Successful transactions:        5047
    Failed transactions:	           0
    Longest transaction:	        0.13
    Shortest transaction:	        0.02    
    
# Django isomorphic template
        
    Transactions:		        5761 hits
    Availability:		      100.00 %
    Elapsed time:		       29.77 secs
    Data transferred:	        3.12 MB
    Response time:		        0.05 secs
    Transaction rate:	      193.52 trans/sec
    Throughput:		        0.10 MB/sec
    Concurrency:		        9.99
    Successful transactions:        5761
    Failed transactions:	           0
    Longest transaction:	        0.12
    Shortest transaction:	        0.02
        