#!/bin/sh -l
set -x
uname -a 
cat /etc/issue
let i=0;
yum -y install libffi-devel
ORIGINALPATH=$PATH
ORIGINALLD_LIBRARY_PATH=$LD_LIBRARY_PATH
for PYBIN in /opt/python/*/bin; do
    export PATH="${PYBIN}":$ORIGINALPATH 
    PYLD=$("${PYBIN}/python" -c "import sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
    export LD_LIBRARY_PATH=$PYLD:$PYBIN/../lib:$PYBIN/../lib64:$ORIGINALLD_LIBRARY_PATH
    sleep 1
    "${PYBIN}/pip" install --upgrade pip twine wheel six  requests cmake auditwheel
    "${PYBIN}/python" do.py  3.2.4 3.2.4 1  auto yes tempbuilddir$i
    let i=i+1
done
out=$?
echo ::set-output name=out::$out
