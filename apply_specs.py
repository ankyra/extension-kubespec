#!/usr/bin/env python

import os
import sys
import json
import glob
import subprocess
import urllib
sys.path = ["deps/_/stdlib/"] + sys.path
from escape import path

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

kubectl_path = "kubectl"

if not path.is_binary_on_path("kubectl"):
    print "kubectl binary is not on PATH"
    url = "https://storage.googleapis.com/kubernetes-release/release/v1.6.4/bin/linux/amd64/kubectl"
    print "Downloading kubectl from", url
    urllib.urlretrieve(url, "kubectl")
    os.chmod("kubectl", 0755)
    kubectl_path = os.path.realpath("./kubectl")
    path.add_binary_to_path(kubectl_path)
else:
    print "Found kubectl binary on path. Skipping download"


for spec in specs:
    print "Deploying Kubernetes spec", spec
    print
    sys.stdout.flush()
    cmd = [kubectl_path, "--kubeconfig", kubecfg_path, "apply", "-f", spec]
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
