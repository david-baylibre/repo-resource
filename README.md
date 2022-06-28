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
