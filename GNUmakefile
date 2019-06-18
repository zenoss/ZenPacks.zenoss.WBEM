##############################################################################
#
# Copyright (C) Zenoss, Inc. 2012, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

PYTHON=$(shell which python)
HERE=$(PWD)
PYWBEM_DIR=$(HERE)/src/pywbem-0.14.3
M2CRYPTO_TAR=$(HERE)/src/M2Crypto-0.32.0.tar.gz
PLY_DIR=$(HERE)/src/ply-3.11
ZP_DIR=$(HERE)/ZenPacks/zenoss/WBEM
LIB_DIR=$(ZP_DIR)/lib
BIN_DIR=$(ZP_DIR)/bin
DOC_DIR=$(HERE)/docs

.PHONY: docs


default: egg

egg:
	# setup.py will call 'make build' before creating the egg
	python setup.py bdist_egg

build: ply m2crypto pywbem $(LIB_DIR) $(BIN_DIR)
	cd $(PYWBEM_DIR) ; \
		PYTHONPATH="$(PYTHONPATH):$(LIB_DIR)" \
		$(PYTHON) setup.py install \
		--install-lib="$(LIB_DIR)" \
		--install-scripts="$(BIN_DIR)"

$(LIB_DIR):
	mkdir -p $(LIB_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

ply:
	pip install --install-dir $(ZP_DIR) -e $(PLY_DIR)

m2crypto: ply
	pip install $(M2CRYPTO_TAR)

pywbem: ply m2crypto
	pip install -e $(PYWBEM_DIR)

clean:
	rm -rf lib build dist *.egg-info
	cd $(PYWBEM_DIR) ; rm -rf build dist *.egg-info

test:
	runtests -v ZenPacks.zenoss.WBEM

docs:
	make -C $(DOC_DIR)
