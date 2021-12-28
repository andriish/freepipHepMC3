import requests, tarfile, os, platform, sys
#from distutils import dir_util as _dir_util
from shutil import copyfile
from shutil import copytree

HEPMC3VERSION = sys.argv[1]
HEPMC3DOWNLOADVERSION = sys.argv[2]
HEPMC3PYPIVERSION = sys.argv[3]
PYTHONEXE = sys.argv[4]
UPLOADSRC = sys.argv[5]
BUILDDIR = sys.argv[6]
if PYTHONEXE == "auto":
    PYTHONEXE = sys.executable

TOKEN = str(
    "pypi-"
)
topdir = os.getcwd()
os.mkdir(BUILDDIR)
os.chdir(BUILDDIR)
buildresult = 0
open("HepMC3-" + HEPMC3DOWNLOADVERSION + ".tar.gz", "wb").write(
    requests.get(
        "https://gitlab.cern.ch/hepmc/HepMC3/-/archive/"
        + HEPMC3DOWNLOADVERSION
        + "/HepMC3-"
        + HEPMC3DOWNLOADVERSION
        + ".tar.gz",
        allow_redirects=True,
    ).content
)
tar = tarfile.open("HepMC3-" + HEPMC3DOWNLOADVERSION + ".tar.gz", "r:gz")
tar.extractall()
tar.close()
os.chdir("HepMC3-" + HEPMC3DOWNLOADVERSION)

extradir = os.path.join(topdir, HEPMC3VERSION)
if os.path.isdir(extradir):
    for f in os.listdir(extradir):
        if os.path.isfile(os.path.join(extradir, f)):
            copyfile(os.path.join(extradir, f), os.path.join(os.getcwd(), f))
        if os.path.isdir(os.path.join(extradir, f)):
            copytree(os.path.join(extradir, f), os.path.join(os.getcwd(), f))
            #_dir_util.copy_tree(os.path.join(extradir, f), os.path.join(os.getcwd(), f))

opt = " --build-number="+HEPMC3PYPIVERSION
if sys.platform == "linux" or sys.platform == "linux2":
    opt += " --plat-name manylinux2010_" + platform.machine()
buildresult += os.system(PYTHONEXE + " setup.py sdist bdist_wheel " + opt)
os.chdir("dist")
if UPLOADSRC == "yes":
    print("HepMC3-" + HEPMC3VERSION + ".tar.gz will be uploaded")
else:
    os.remove("HepMC3-" + HEPMC3VERSION + ".tar.gz")

for f in os.listdir(os.getcwd()):
    if os.path.isfile(f):
        if sys.platform == "linux" or sys.platform == "linux2":
            print("Auditwheel call. Actually needed only for the root modules.")
        # We actually don't care about uploading
        #os.system(PYTHONEXE + " -m twine upload " + f + "  -u __token__ -p " + TOKEN)
os.chdir(topdir)
sys.exit(buildresult)
