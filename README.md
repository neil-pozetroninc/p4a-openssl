# p4a-openssl

![openssl](https://img.shields.io/badge/openssl-1.0.2n-brightgreen.svg)

openssl-python package for python-for-android. 

Updated to current OpenSSL version `1.0.2.n` and added x86 support. 

>Note: This requires recompiling cystax python with openssl support, 
this is in [p4a-crystax](https://github.com/frmdstryr/p4a-crystax).


## Usage

With [enaml-native](https://github.com/codelv/enaml-native/), 
activate your apps env and install with pip.

```python

source venv/bin/activate
pip install p4a-openssl

```

> Note: Forgetting to install this recipe in the env will cause p4a to try and install
and build openssl using pip which will fail. 

Next add it to your `package.json`

```json

"dependencies": {
    "python2crystax": "", 
    "enaml-native": "",
    "openssl": "",
}, 

```

Finally rebuild your python dependencies.

```bash

enaml-native build-python

```

Ssl support should now work within the app.


### Donate

This took me several days to implement. If this was helpful to you, 
please consider buying me [a coffee](https://www.codelv.com/donate/) :)

