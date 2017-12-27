#! /usr/bin/env bash
##############################################################################
#
# Copyright (C) Zenoss, Inc. 2017, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################


MYPATH=`python -c "import os.path; print os.path.realpath('$0')"`
THISDIR=`dirname $MYPATH`
PRGHOME=`dirname $THISDIR`
PRGNAME=wbem-query.py

HOST=$1;
USERNAME=$2;
PASSWORD=$3;


# SERVER_INFO
python $PRGHOME/utilities/$PRGNAME --host "${HOST}" --username "${USERNAME}" --password "${PASSWORD}" --classname "CIM_ComputerSystem";
python $PRGHOME/utilities/$PRGNAME --host "${HOST}" --username "${USERNAME}" --password "${PASSWORD}" --classname "CIM_OperatingSystem";

