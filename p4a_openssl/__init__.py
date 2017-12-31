from functools import partial

from pythonforandroid.toolchain import Recipe, shprint, current_directory
import sh


class OpenSSLRecipe(Recipe):
    version = '1.0.2h'
    url = 'https://www.openssl.org/source/openssl-{version}.tar.gz'
    name = 'openssl'

    def should_build(self, arch):
        return not self.has_libs(arch, 'libssl.so',# + self.version + '.so',
                                 'libcrypto.so')# + self.version + '.so')

    def check_symbol(self, env, sofile, symbol):
        nm = env.get('NM', 'nm')
        syms = sh.sh('-c', "{} -gp {} | cut -d' ' -f3".format(
                nm, sofile), _env=env).splitlines()
        if symbol in syms:
            return True
        print('{} missing symbol {}; rebuilding'.format(sofile, symbol))
        return False

    def get_recipe_env(self, arch=None):
        env = super(OpenSSLRecipe, self).get_recipe_env(arch)
        env['OPENSSL_VERSION'] = self.version
        env['CFLAGS'] += ' ' + env['LDFLAGS']
        env['CC'] += ' ' + env['LDFLAGS']
        return env

    def select_build_arch(self, arch):
        aname = arch.arch
        if 'arm64' in aname:
            return 'linux-aarch64'
        if 'v7a' in aname:
            return 'android-armv7'
        if 'arm' in aname:
            return 'android'
        #if 'x86_64' in aname:
        #    return 'android-x86_64'
        if 'x86' in aname:
            return 'android-x86'
        return 'linux-armv4'

    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            # sh fails with code 255 trying to execute ./Configure
            # so instead we manually run perl passing in Configure
            perl = sh.Command('perl')
            buildarch = self.select_build_arch(arch)
            shprint(perl, 'Configure', 'shared', 'no-dso', 'no-krb5', 'no-ssl2', 'no-ssl3', 'no-comp', 'no-hw', buildarch, _env=env)

            #: No longer required for 1.0.2n
            #self.apply_patch('disable-sover.patch', arch.arch)
            #self.apply_patch('rename-shared-lib.patch', arch.arch)

            #: Patch openssl 1.0.2n
            #self.apply_patch('drop-cpuid.patch', arch.arch)

            # check_ssl = partial(self.check_symbol, env, 'libssl' + self.version + '.so')
            check_crypto = partial(self.check_symbol, env, 'libcrypto.so')# + self.version + '.so')
            while True:
                shprint(sh.make, 'build_libs', _env=env)
                if all(map(check_crypto, ('SSLeay', 'MD5_Transform', 'MD4_Init'))):
                    break
                shprint(sh.make, 'clean', _env=env)

            self.install_libs(arch, 'libssl.so',# + self.version + '.so',
                              'libcrypto.so')# + self.version + '.so')


def get_recipe():
    return (OpenSSLRecipe(), __file__)
