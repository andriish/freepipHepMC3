# Container image that runs your code
FROM quay.io/pypa/manylinux2010_x86_64
#cp27-cp27m
#cp27-cp27mu
#cp35-cp35m
#cp36-cp36m
#cp37-cp37m
#cp38-cp38
#cp39-cp39



#Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

#Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
