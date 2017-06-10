#!/usr/bin/env python

import os
import sys
import json
import glob
import subprocess

env = os.environ

kubecfg_path = env['INPUT_kubecfg_path']
specs = env['INPUT_kube_spec_files']
specs = "[]" if specs == "" else specs

try:
    specs = json.loads(specs)
except Exception, e:
    print "Couldn't parse specs."
    print e
    sys.exit(1)


if specs == []:
    for f in glob.glob("*.yaml"):
        specs.append(f)
    for f in glob.glob("*.yml"):
        if f not in ["escape.yml", "circle.yml"]:
            specs.append(f)


for spec in specs:
    print "Deploying Kubernetes spec", spec
    print
    sys.stdout.flush()
    cmd = ["kubectl", "--kubeconfig", kubecfg_path, "apply", "-f", spec]
    try:
        subprocess.check_output(cmd)
    except subprocess.CalledProcessError, e:
        print "Failed to run '%s'" % " ".join(cmd)
        print e
        sys.exit(1)
    print "Successfully applied", spec

if specs == []:
    print "Didn't find any Kubernetes spec files to apply. You can either supply them "
    print "in the `kube_spec_files` variable or drop some .yml files in the current directory."
