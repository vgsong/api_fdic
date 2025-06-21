## FDIC API

Small API from FDIC.
CLI that pulls data based on Quarterly Report Date and Bank Cert Number.
ouput in csv format

Other reports will be included. Currently only endpoint for financials.
eventually from CLI to PYQt05 (still learning)

--------------------------------------------

-/institutions   - get financial institutions  
-/locations      - get institution locations  
-/history        - get detail on structure change events  
-/financials     - get financial information for FDIC Insured Insitutions -- currently main url only pulls data from /financials  

-/summary        - get historical aggregate data by year  
-/failures       - get detail on historial bank failures from 1934 to present  
-/sod            - get summary of deposits information for FDIC Insured Institutions  
-/demographics   - get summary of demographic information  




----- MAIN MENU --------

1 - 'GETDATA'       - get user input and GET api call from FDIC  
2 - 'LOOKUPCERT'    - looks up bank cert number  
9 - 'OPENDIR'       - current opens main root dir  (based on env var)  
0 - 'QUIT'          - exit  