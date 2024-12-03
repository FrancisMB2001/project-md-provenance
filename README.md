# Provenance Testing Project - MD Project

Small uvicorn / FastAPI project built with python to test the use of the provenance package. Specifically designed for the MD (Data Modelling) course. 

**Developed using Co-pilot.** 


## Instructions to run the project 
- Create virtual env 
```bash
python3 -m venv prov-testing
source prov-testing/bin/activate  
pip install fastapi uvicorn provenance
```
- Start the api server 
```bash
uvicorn main:app --reload
```
- Run tests 
```bash
python3 test_provenance.py
```

