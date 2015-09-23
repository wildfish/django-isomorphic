#!/usr/bin/env bash

cd ./tests/templates/
npm install react
cd ..
cd ..


# Start the template server
node ./javascript/dist/template-server.js socketPath=./template-server.sock &

nohup bash -c "node ./javascript/dist/template-server.js socketPath=./template-server.sock 2>&1 &" && sleep 2
./runtests.sh
