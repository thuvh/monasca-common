#!/bin/bash
find / -name "*mvn*" 2> /dev/null
VERSION=`/usr/bin/mvn -v | grep "Apache Maven 3"`
if [ -z "${VERSION}" ]; then
   sudo apt-get install maven
fi
echo $*
shift
echo $*
cd java
/usr/bin/mvn $*
