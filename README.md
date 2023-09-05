## TODO
background task for bulk insert + redis queue  

## HOW TO RUN
To dev:  
create a python venv, start it, install dependencies and run dev.sh:  
<pre>
python -m venv venv
source venv/bin/activate
pip install -r dev-requirements.txt
source dev.sh
</pre>

To test:

create a python venv, start it, install dependencies and run test.sh:
<pre>
python -m venv venv
source venv/bin/activate
pip install -r dev-requirements.txt
source test.sh
</pre>

To run:
<pre>
source run.sh
</pre>
Application should respond at:  
    http://localhost:9999
