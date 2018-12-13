# coding=utf-8

import os, sys, glob
import pkg_resources
from modulegraph import find_modules
from distutils.sysconfig import get_config_vars, get_config_var

import logging
FORMAT = '%(relativeCreated)d %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(os.path.basename(__file__))

_DefaultExcludes = ['pip', 'setuptools', 'pkg_resources', 'distutils', 'logging' ]
_DefaultExcludes.extend( sys.builtin_module_names )
try:
    _DefaultExcludes.append(globals().get('__spec__').name)
except:
    pass

class helper:
    SitePackages = [ p for p in sys.path if p.find(os.path.normpath('/site-packages')) > 0]
    PythonLib = set(get_config_vars('DESTSHARED', 'DESTLIB', 'LIBDEST', 'BINLIBDEST')) - set([None, ''])

    is_win = sys.platform.startswith('win')
    if is_win:
        SitePackages = [ p.lower() for p in SitePackages ]
        PythonLib = [ p.lower() for p in PythonLib ]
        Libdest = get_config_var('LIBDEST')
        if Libdest and os.path.isdir(Libdest):
            Dllpath = os.path.join(os.path.dirname(Libdest), 'dlls').lower()
            PythonLib.append(Dllpath)
    logger.info("SitePackages:%s", SitePackages)
    logger.info("PythonLib:%s", PythonLib)

    @staticmethod
    def source_type(filename):
        if not os.path.isabs(filename):
            return 'UNKOWN'
        fname = filename.lower() if helper.is_win else filename
        for pth in helper.SitePackages:
            if fname.startswith(pth):
                return 'SitePackages'
        for pth in helper.PythonLib:
            if fname.startswith(pth):
                return 'PythonLib'
        return 'UNKOWN'

    @staticmethod
    def get_toplevel_modules_path(filename):
        curr_dir = os.path.dirname(os.path.abspath(filename))
        pattern = '__init__.py'

        # Try max. 10 levels up.
        try:
            for i in range(10):
                files = set(os.listdir(curr_dir))
                # 'curr_dir' is still not top-leve go to parent dir.
                if pattern in files:
                    curr_dir = os.path.dirname(curr_dir)
                # Top-level dir found - return it.
                else:
                    return curr_dir
        except IOError:
            pass
        # No top-level directory found or any error.
        return None

def _write_modules(zfile, modules, basepath):
    for (ty, nm, fp) in modules:
        nmbase, dst = nm.split('.',1)[0] , None
        if nmbase.find(os.path.sep) >= 0:
            dst = os.path.relpath(fp, basepath)
        else:
            i = os.path.normpath(fp).find(os.path.normcase('/'+nmbase ))
            assert i > 0 , "path:{0}, module base:{1}, type:{2}".format(fp, nmbase, ty)
            dst = fp[i+1:]
        logger.info("package module:<%s> , from %s -> %s", nm, fp, dst)
        try:
            zfile.write(fp, dst)
        except Exception as e:
            logger.warning(e)


def _write_files(zfile, binaries_or_datas, workingdir):
    toc_datas = set()
    for src_root_path_or_glob, trg_root_dir in binaries_or_datas:
        if not trg_root_dir:
            raise SystemExit("Empty DEST not allowed when adding binary and data files. "
                             "Maybe you want to used %r.\nCaused by %r." %(os.curdir, src_root_path_or_glob))

        trg_root_dir = os.path.join(os.path.basename(workingdir), trg_root_dir)

        # Convert relative to absolute paths if required.
        if workingdir and not os.path.isabs(src_root_path_or_glob):
            src_root_path_or_glob = os.path.join(workingdir, src_root_path_or_glob)
        # Normalize paths.
        src_root_path_or_glob = os.path.normpath(src_root_path_or_glob)
        if os.path.isfile(src_root_path_or_glob):
            src_root_paths = [src_root_path_or_glob]
        else:
            # List of the absolute paths of all source paths matching the current glob.
            src_root_paths = glob.glob(src_root_path_or_glob)

        if not src_root_paths:
            msg = 'Unable to find "%s" when adding binary and data files.' % ( src_root_path_or_glob)
            raise SystemExit(msg)

        for src_root_path in src_root_paths:
            if os.path.isfile(src_root_path):
                # Normalizing the result to remove redundant relative
                # paths (e.g., removing "./" from "trg/./file").
                toc_datas.add( (os.path.normpath(os.path.join(trg_root_dir, os.path.basename(src_root_path))),
                    os.path.normpath(src_root_path)) )
            elif os.path.isdir(src_root_path):
                for src_dir, src_subdir_basenames, src_file_basenames in os.walk(src_root_path):
                    assert src_dir.startswith(src_root_path)
                    trg_dir = os.path.normpath(os.path.join(
                        trg_root_dir,
                        os.path.relpath(src_dir, src_root_path)))

                    for src_file_basename in src_file_basenames:
                        src_file = os.path.join(src_dir, src_file_basename)
                        if os.path.isfile(src_file):
                            # Normalize the result to remove redundant relative
                            # paths (e.g., removing "./" from "trg/./file").
                            toc_datas.add((
                                os.path.normpath(os.path.join(trg_dir, src_file_basename)),
                                os.path.normpath(src_file)))

    for (dst, src) in toc_datas:
        logger.info("package file: from %s -> %s", src, dst)
        zfile.write(src, dst)

def _write_requires(zfile, requires):
    if not requires:
        return
    reqfile = os.path.splitext(zfile.filename)[0] + '-requires.txt'
    with open(reqfile, 'w') as o:
        for pkg, version in requires.items():
            l = '=='.join([pkg, version])
            logger.info('add require module: %s', l)
            o.write(l + '\n')
    dst = 'requires.txt'
    logger.info("package file: from %s -> %s", reqfile, dst)
    zfile.write(reqfile, dst)

def package(scripts, name=None, pathex=None, datas=None, binaries=None, includes=None, excludes=None):
    '''
     usage: package(__file__, datas=[(src,dst), (src, dst), ])
    :param scripts: scripts file to parse from
    :param name:  zip file name
    :param pathex:
    :param datas:
    :param binaries:
    :param includes:
    :param excludes:
    :return: the zipfile path
    '''
    excludes, includes, inputs  = excludes or [], includes or [], []
    scripts = [scripts] if isinstance(scripts, str) else scripts
    if not isinstance(scripts, (tuple, list)):
        raise ValueError("scripts parameters must be str or tuple or list ")

    for script in scripts:
        # Normalize script path.
        script = os.path.normpath(script)
        if not os.path.exists(script):
            raise ValueError("script '%s' not found" % script)
        inputs.append(helper.get_toplevel_modules_path(script))

    toplevelpath = inputs[0]
    inputs.extend(sys.path + (pathex or []))
    basepath = os.path.abspath(os.path.dirname(scripts[0]))

    installed_pkgs = dict((d.project_name, d.version) for d in pkg_resources.working_set)

    logger.info("trying to analysis dependents , please wait ...")
    mf = find_modules.find_modules(scripts=scripts, includes=includes, excludes=excludes + _DefaultExcludes, path=inputs)
    requires, depends_thirds, depends_selfmod = {}, [], []
    for m in mf.flatten() :
        ty, nm, fn = type(m).__name__, m.identifier, m.filename
        if not ty in ['MissingModule', 'AliasNode', 'BuiltinModule', 'ExcludedModule']:
            logger.info("check type:%s, module:%s, path:%s", ty, nm, fn)
            ver = installed_pkgs.get(nm, None)
            if ver:
                requires[nm] = ver
                continue
            nmbase = nm.split('.', 1)[0]
            ver = installed_pkgs.get(nmbase, None)
            if ver:
                requires[nmbase] = ver
                continue
            sourcetype = helper.source_type(fn)
            if sourcetype == 'PythonLib':
                logger.debug('###########> ignore python lib type:%s, module:<%s>, %s',ty, nm, fn )
                pass
            elif sourcetype == 'SitePackages':
                depends_thirds.append((ty, nm, fn))
                logger.debug('----------> add site-packages type:%s, module:<%s>, %s',ty, nm, fn )
            elif sourcetype == 'UNKOWN':
                depends_selfmod.append((ty, nm, fn))
                logger.debug('----------> add self modules type:%s, module:<%s>, %s',ty, nm, fn )

    import zipfile
    zfilepath = name if name else os.path.join(toplevelpath, os.path.basename(scripts[0]))
    zfilepath = os.path.splitext(zfilepath)[0] + '.zip'
    logger.info("trying to zip dependents to %s", zfilepath )
    with zipfile.ZipFile(zfilepath, 'w') as zfile:
        _write_modules(zfile, depends_thirds + depends_selfmod, toplevelpath )
        _write_files(zfile, (datas or []) + (binaries or []) , basepath)
        _write_requires(zfile, requires)
    logger.info("dependents have been packaged to %s", zfilepath)
    return zipfile
