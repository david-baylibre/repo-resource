# Repo resource

Track changes in a [repo](https://gerrit.googlesource.com/git-repo/+/master/#repo) project.

## Source configuration

* `url`: *Required.* manifest repository location.

* `revision`: manifest branch or revision (use `HEAD` for default).

* `name`: initial manifest file.


### Example

Resource configuration for a public project using repo (Android)

```yaml
resource_types:
- name: repo
  type: registry-image
  source:
    repository: mkorpershoek/repo-resource

resources:
- name: aosp
  type: repo
  check_every: 2h # default of 1min seems too frequent
  source:
    url: https://android.googlesource.com/platform/manifest
    branch: master
    name: default.xml
```

## Contributing/development

### Rebuilding the docker image

```
make
```

### Publish to docker hub

```
make push
```

### Unit testing

Use `tox` for running the unit tests:
```
tox
```
See the [tox wiki](https://tox.wiki/en/latest/) for more details

Note that it's also possible to run them without `tox` using `make test`
