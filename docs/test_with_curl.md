## Testing

if you want to test the `thoth_thamos_advise` webhook we have invented, use the fixture `thoth_thamos_advise_finished_1.json`
and

```shell
curl -X POST -v -k http://qeb-hwt-aicoe-prod-bots.cloud.paas.psi.redhat.com/ -d '{
    "action": "finished",
    "installation": {
        "id": 6181026
    },
    "repo_url": "https://api.github.com/repos/thoth-station/stub-api",
    "check_run_id": 394768387,
    "adviser_result": {
        "text": "This text goes into the details section of the Check.\n\nUt quis occaecat commodo incididunt aliquip aliquip occaecat sit anim irure.",
        "summary": "This is a Developer Preview Service.\n\nId exercitation cillum ex labore. Culpa culpa minim aute ad nulla nostrud elit"
    }
}' -H 'X-GitHub-Event: thoth_thamos_advise' -H 'X-GitHub-Delivery: random_uuid' -H 'Content-Type: application/json' -H 'X-Hub-Signature: sha1=973e2b82c196a1cef0cce179381201896a8ec8f1'
```
