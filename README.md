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

### Local concourse instance and docker registry.

It's also possible to use a local docker registry (instead of docker hub) for development.
This allows closer "end-to-end" testing on a development workstation.

This section assumes that you've installed `docker` and `docker-compose` as documented in
https://concourse-ci.org/getting-started.html

1. Start by running a concourse development instance and install `fly`:
   ```
   curl -O https://concourse-ci.org/docker-compose.yml
   docker-compose up -d

   curl 'http://localhost:8080/api/v1/cli?arch=amd64&platform=linux' -o fly \
       && chmod +x ./fly && mv ./fly /usr/local/bin/

   fly -t tutorial login -c http://localhost:8080 -u test -p test
   ```
   See https://concourse-ci.org/quick-start.html#docker-compose-concourse for details

2. Start your local docker registry:
   ```
   docker run --network dev-instance_default -d -p 5000:5000 --name registry registry:2
   ```
   See https://www.docker.com/blog/how-to-use-your-own-registry-2/ for more information

3. Rebuild and publish your docker image to the local registry:
   ```
   make dev-push
   ```

4. Get the IP address of your `registry` container. This is needed because the `concourse/concourse`
   container seems unable to lookup by hostname address:
   ```
   docker run --network dev-instance_default -it ubuntu /bin/bash
   apt update && apt install -y inetutils-ping
   ping registry
   # PING registry (172.20.0.4): 56 data bytes
   ```
   Note the ip address (`172.20.0.4` in this example).

5. Publish a development job with `fly` using the [development `pipeline.yml`](./development/pipeline.yml)
   ```
   fly -t tutorial set-pipeline -p development -c development/pipeline.yml
   fly -t tutorial unpause-pipeline -p development
   fly -t tutorial check-resource -r development/aosp-kernel
   ```
