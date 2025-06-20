## FDIC API

Small API from FDIC website.
CLI that pulls data based on Quarter Report and Bank Cert Number from financials table.
Other tables will be included in the CLI
eventually into PYQt05

--------------------------------------------

-/institutions   - get financial institutions  
-/locations      - get institution locations  
-/history        - get detail on structure change events  
-/financials     - get financial information for FDIC Insured Insitutions -- currently main url only pulls data from /financials  
-/summary        - get historical aggregate data by year  
-/failures       - get detail on historial bank failures from 1934 to present  
-/sod            - get summary of deposits information for FDIC Insured Institutions  
-/demographics   - get summary of demographic information  



1 - 'GETDATA'       - get user input and GET api call from FDIC  
2 - 'LOOKUPCERT'    - looks up bank cert number  
9 - 'OPENDIR'       - current opens main root dir  (based on env var)  
0 - 'QUIT'          - exit  