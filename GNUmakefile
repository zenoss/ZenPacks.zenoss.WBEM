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
ZP_DIR=$(HERE)/ZenPacks/zenoss/WBEM
LIB_DIR=$(ZP_DIR)/lib
BIN_DIR=$(ZP_DIR)/bin
DEPS=$(ZP_DIR)/dependencies
DOC_DIR=$(HERE)/docs

PLY_TAR=$(HERE)/src/ply-3.11.tar.gz
TYPING_TAR=$(HERE)/src/typing-3.6.6.tar.gz
PYWBEMZ_TAR=$(HERE)/src/pywbemz-0.14.3.tar.gz
M2CRYPTO_TAR=$(HERE)/src/m2crypto-0.38.0.tar.gz
PLY_DEP=$(DEPS)/ply-3.11
TYPING_DEP=$(DEPS)/typing-3.6.6
PYWBEMZ_DEP=$(DEPS)/pywbemz-0.14.3
M2CRYPTO_DEP=$(DEPS)/m2crypto-0.38.0

.PHONY: docs

default: egg

egg:
	# setup.py will call 'make build' before creating the egg
	python setup.py bdist_egg

build: dependencies $(LIB_DIR) $(BIN_DIR)
	@echo

dependencies:
	mkdir -p $(DEPS) $(PLY_DEP) $(TYPING_DEP) $(M2CRYPTO_DEP) $(PYWBEMZ_DEP)
	PYTHONPATH="$(PYTHONPATH):$(PLY_DEP)"      easy_install --no-deps --install-dir="$(PLY_DEP)"      $(PLY_TAR)
	PYTHONPATH="$(PYTHONPATH):$(TYPING_DEP)"   easy_install --no-deps --install-dir="$(TYPING_DEP)"   $(TYPING_TAR)
	PYTHONPATH="$(PYTHONPATH):$(M2CRYPTO_DEP)" easy_install --no-deps --install-dir="$(M2CRYPTO_DEP)" $(M2CRYPTO_TAR)
	PYTHONPATH="$(PYTHONPATH):$(PYWBEMZ_DEP)"  easy_install --no-deps --install-dir="$(PYWBEMZ_DEP)"  $(PYWBEMZ_TAR)

$(LIB_DIR):
	mkdir -p $(LIB_DIR)
	PYTHONPATH="$(PYTHONPATH):$(LIB_DIR)"

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

clean:
	rm -rf lib build dist *.egg-info
	cd $(PYWBEM_DIR) ; rm -rf build dist *.egg-info

test:
	runtests -v ZenPacks.zenoss.WBEM

docs:
	make -C $(DOC_DIR)
