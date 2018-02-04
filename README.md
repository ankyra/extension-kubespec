# Escape extension for Kubernetes specs

This is an Escape extension that will submit Kubernetes specs to a Kubernetes
cluster.

Please see https://escape.ankyra.io for the full Escape documentation.

## Usage

### Submit files

```
name: my-release

extends:
- extension-kubespec

inputs
- id: kube_spec_files
  default:
  - deployment.yml
  - service.yml
```

### Combined with templating

```
name: my-release

extends:
- extension-kubespec

inputs
- id: kube_spec_files
  default:
  - deployment.yml
  - service.yml
- id: my_input
  default: hello world

templates:
- file: deployment.yml.tpl
- file: service.yml.tpl
  mapping:
    service_name: $this.inputs.my_input
```

## License

```
Copyright 2017, 2018 Ankyra

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
