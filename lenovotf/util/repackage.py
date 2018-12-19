import os, sys
import zipfile
import shutil

import logging
FORMAT = '%(relativeCreated)d %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(os.path.basename(__file__))


def _repackage_with_requires(zfile, reqfile, extra_args = None):
    from pip._internal.commands.install import InstallCommand
    workdir = os.path.dirname(reqfile)
    default_args = '--root {0} --prefix vendors --ignore-installed -r {1}'.format(workdir, reqfile)
    logger.info("install to temp dir :%s", workdir)
    args = default_args.split() + ( extra_args or [] )
    InstallCommand().main(args)
    origzip = os.path.abspath(zfile)
    assemblezip = os.path.splitext(origzip)[0] + '_with_dependences.zip'
    shutil.copyfile(origzip, assemblezip )
    with zipfile.ZipFile(assemblezip, 'a') as zip:
        os.chdir(workdir)
        for root, _, files in os.walk('vendors'):
            for name in files:
                filepath = os.path.join(root, name)
                zip.write(filepath)
    return assemblezip

def repackage(zfile, options = None):
    try:
        zip = zipfile.ZipFile(zfile, 'r')
    except FileNotFoundError:
        raise SystemExit("File not found error: " + zfile)
    pdir, basename = os.path.dirname(zfile) , os.path.basename(zfile)
    tmpdir  = os.path.splitext(basename)[0] + '_tmp_'
    workdir = os.path.abspath( os.path.join( pdir, tmpdir) )
    try:
        reqfile = zip.extract('requires.txt', workdir)
    except KeyError :
        logger.info("requires.txt not exist, need not repackage")
        sys.exit(0)

    assemblezip = _repackage_with_requires(zfile, reqfile, options)
    logger.info("package all to %s", assemblezip)

if __name__ == '__main__':
    # repackage('../testimp.zip', ['--no-deps'])
    if len(sys.argv) < 3:
        print("usage: {0} <zipfile>".format(sys.argv[0]))
        sys.exit(-1)

    repackage(sys.argv[1], sys.argv[2:])