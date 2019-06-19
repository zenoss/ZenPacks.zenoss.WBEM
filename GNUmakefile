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
PYWBEMZ_TAR=$(HERE)/src/pywbemz-0.14.3.tar.gz
M2CRYPTO_TAR=$(HERE)/src/M2Crypto-0.32.0.tar.gz
PLY_TAR=$(HERE)/src/ply-3.11.tar.gz
ZP_DIR=$(HERE)/ZenPacks/zenoss/WBEM
LIB_DIR=$(ZP_DIR)/lib
BIN_DIR=$(ZP_DIR)/bin
DOC_DIR=$(HERE)/docs

.PHONY: docs


default: egg

egg:
	# setup.py will call 'make build' before creating the egg
	python setup.py bdist_egg

build: ply m2crypto pywbemz $(LIB_DIR) $(BIN_DIR)
	@echo

$(LIB_DIR):
	mkdir -p $(LIB_DIR)
	PYTHONPATH="$(PYTHONPATH):$(LIB_DIR)"

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

ply: $(LIB_DIR) $(BIN_DIR)
	PYTHONPATH="$(PYTHONPATH):$(LIB_DIR)" \
	easy_install --no-deps --install-dir="$(LIB_DIR)" --script-dir="$(BIN_DIR)" $(PLY_TAR)

m2crypto: ply
	PYTHONPATH="$(PYTHONPATH):$(LIB_DIR)" \
	easy_install --no-deps --install-dir="$(LIB_DIR)" --script-dir="$(BIN_DIR)" $(M2CRYPTO_TAR)

pywbemz: ply m2crypto
	PYTHONPATH="$(PYTHONPATH):$(LIB_DIR)" \
	easy_install --no-deps --install-dir="$(LIB_DIR)" --script-dir="$(BIN_DIR)" $(PYWBEMZ_TAR)

clean:
	rm -rf lib build dist *.egg-info
	cd $(PYWBEM_DIR) ; rm -rf build dist *.egg-info

test:
	runtests -v ZenPacks.zenoss.WBEM

docs:
	make -C $(DOC_DIR)
