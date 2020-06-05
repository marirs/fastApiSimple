# fastAPI boilerplate

This project is to use fastAPI with just an API Key in the URL Path. This can be used for simple API microservices where JWT/API Header/etc. is not required.

#### Requirements
- Python 3.8+
- MongoDB

- Deploying the server
```bash
mkvirtualenv --python=`which python3.8` fastApiSimple
cd /path/to/fastApiSimple
setvirtualenvproject
```

- Running the server in development
```bash
$ ./server.sh run
```

#### Endpoints
- user: /api/{api_key}/user - User list
- docs: /api/{api_key}/docs - fastApi Documentation
---
 
Author: Sriram
