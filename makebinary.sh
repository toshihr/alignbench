#!/bin/sh
rm myapp.zip
zip myapp.zip __main__.py alignbench/*.py alignbench/*.pyc
echo '#!/usr/bin/env python' > myapp
cat myapp.zip >>myapp
chmod +x myapp
