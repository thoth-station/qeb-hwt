## Testing

if you want to test the `thoth_thamos_advise` webhook we have invented, use the fixture `thoth_thamos_advise_finished_1.json`
and

```shell
curl -X POST -v -k http://qeb-hwt-aicoe-prod-bots.cloud.paas.psi.redhat.com/ -d '{
    "action": "finished",
    "installation": {
        "id": 6181026
    },
    "repo_url": "https://api.github.com/repos/thoth-station/Qeb-Hwt",
    "check_run_id": 394815661,
    "payload": {
        "analysis_id": "adviser-f1d5d010"
    }
}
' -H 'X-GitHub-Event: thoth_thamos_advise' -H 'X-GitHub-Delivery: random_uuid' -H 'Content-Type: application/json' -H 'X-Hub-Signature: sha1=some_sha'
```
