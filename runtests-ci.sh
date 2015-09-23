#!/usr/bin/env bash

cd ./tests/templates/
npm install react
make
cd ..
cd ..

# Start the template server
nohup bash -c "node ./javascript/dist/template-server.js socketPath=./template-server.sock 2>&1 &" && sleep 2

./runtests.sh
