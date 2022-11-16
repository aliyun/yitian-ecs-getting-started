FROM node:18-alpine
WORKDIR /benchmark
COPY cli.js .
COPY parallel.sh parallel.sh

ENTRYPOINT node --max-semi-space_size=128 cli.js | tail -n 1 | awk '{print "sp", $3}' && ./parallel.sh

