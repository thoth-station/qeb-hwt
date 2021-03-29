# Changelog for Qeb-Hwt

## [0.1.0] - 2019-Nov-20 - goern

### Added

all the things that you see...

## Release 0.3.0 (2020-08-11T06:04:07)
* :pushpin: Automatic update of dependency pytest from 6.0.0rc1 to 6.0.1 (#90)
* :pushpin: Automatic update of dependency pytest from 6.0.0rc1 to 6.0.1 (#89)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.2.0 to 0.2.4 (#88)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.2.0 to 0.2.4 (#87)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.2.0 to 0.2.4 (#86)
* :pushpin: Automatic update of dependency pytest from 6.0.0rc1 to 6.0.1 (#85)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#84)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#83)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.2.0 to 0.2.4 (#82)
* :pushpin: Automatic update of dependency octomachinery from 0.2.1 to 0.2.2 (#81)
* :pushpin: Automatic update of dependency thoth-common from 0.14.2 to 0.16.0 (#80)
* :pushpin: Automatic update of dependency octomachinery from 0.2.1 to 0.2.2 (#79)
* Adjust imports (#75)
* :truck: include aicoe-ci configuration file (#69)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#74)
* :pushpin: Automatic update of dependency thoth-common from 0.14.1 to 0.14.2 (#71)
* :pushpin: Automatic update of dependency pandas from 1.0.5 to 1.1.0rc0 (#72)
* :pushpin: Automatic update of dependency pytest from 5.4.3 to 6.0.0rc1 (#73)
* Upgraded to Python 3.8 (#68)
* Remove templates handled by thoth-application (#66)
* Move utils (#65)
* Moved to report-processing (#64)
* Create OWNERS
* Keep wf for SLI
* Add info about runtime environment
* Add return values
* Remove empty part of reports
* Introduce formatting of json for adviser report
* Add packages
* added a 'tekton trigger tag_release pipeline issue'
* Use THOTH_ in env
* Remove imagestreams
* Use workflow-helper
* Update qeb-hwt-template.yaml
* update version
* Use thoth-toolbox and correct exceptions
* Adjust exception message
* Insert template file to be provided and link to readme
* Remove default yaml, thamos will provide error with missing thoth config
* handle FileLoadError
* Little change
* Modify format file for schema doc
* Move Installation doc to docs repo
* Add usage to README file
* Use safe_load to load configuration
* removed black and pre-commit from [dev]
* added Kebechet configuration
* Add shallow clone
* Adjust inputs to read from thoth yaml
* Setup workflow TTL strategy to reduce preassure causing OOM
* Update name in qeb-hwt workflow
* Adjust report error to include errors if they are present
* Logger name
* Handling VCS use instead of package index from users
* Missing imports and add variable
* Add steps tutorial
* Thamos exceptions handling
* Tutorial to install Qeb-Hwt App
* :green_heart: fixed to coala errors
* add max characters allowed in text by GitHub
* Adjust check-run-url
* Update docs
* Add error messages if adviser fails
* Add default .thoth.yaml if user does not provides it
* Adjust check run in progress, modify justification and insert attempts
* adjust adviser urljoin
* re add origin for Adviser syncs and tracking
* thamos really needs UPPERCASE LETTERS?!!?
* Adjust parameters for thamos workflow finished
* some more logging
* empty
* Use correct repo_url
* Replaced Pipfile.lock
* Correct input
* fixed the json data and removed the sha from the curl call
* added exception handling so that we dont raise it to sentry
* Revert SA
* Use user-api service account
* fixed typo
* removed tracing stuff
* Adjust POST request
* added jaeger for tracing (NOT_IMPLEMENTED), minor fixes
* minor tweaks
* Adjust name
* Use latest Thamos image for GitHub App
* Standardize parameters for Thamos
* fixed some coala errors
* Adjust templates for new architecture
* Add docs
* relocked dependencies
* Small changes in templates
* Add draft
* Adjust User-API call
* empty
* User API Call from workflow
* ...
* added argo-workflow-sdk from my personal pypi
* empty
* Trigger thoh advise workflow on PR event
* Handle thoth_thamos_advise finished event
* corrected the url
* renamed to make coala happy
* renamed to make coala happy
* finishing check-run based on workflow:finished webhook event
* finishing check-run based on workflow:finished webhook event
* minor tweaks
* added the OpenShift secrets to be ignored.
* minor tweaks
* Changed payload from string to object
* Added thoth_thamos_advise payload fixture
* new method signature
* added some TODO
* removed `organizaion` as a required argument
* relocked due to octomachinery 0.1.2 release
* fixed a typo, fixing snake filename issues
* reorganized stuff to have templates for everything
* Fixed coala issues
* Added ultrahook image build template
* :sparkles: added on_pr_open_or_sync()
* Added ultrahook container to the deploymentconfig
* renameds some parameters
* removed the comments
* reformatting
* :sparkles: added on_advise_workflow_finished() as a stub
* removed 'double-quote-string-fixer' as it conflicts with black and our standards
* :sparkles: added pre-commit and updated dependencies
* Fixed invalid deployment trigger
* :memo: dumping drafts
* Happy New Year!
* :green_heart: fixed coala errors
* :green_heart: we have no tests by now...
* :sparkles: some work
* 🔥 fix file prevents loading other thoth. modules from PYTHONPATH
* rearranged the template project
* rearranged the template project

## Release 0.3.1 (2020-09-24T17:13:46)
### Features
* Add new maintainer (#111)
### Other
* remove TODO already solved (#102)
### Automatic Updates
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#109)
* :pushpin: Automatic update of dependency thoth-common from 0.19.0 to 0.20.0 (#108)
* :pushpin: Automatic update of dependency octomachinery from 0.2.2 to 0.3.0 (#107)
* :pushpin: Automatic update of dependency pytest from 6.0.1 to 6.0.2 (#105)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.3.0 to 0.3.4 (#104)
* :pushpin: Automatic update of dependency thoth-common from 0.17.2 to 0.19.0 (#103)
* :pushpin: Automatic update of dependency thoth-common from 0.16.1 to 0.17.2 (#101)
* :pushpin: Automatic update of dependency pylint from 2.5.3 to 2.6.0 (#99)
* :pushpin: Automatic update of dependency pylint from 2.5.3 to 2.6.0 (#98)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.2.4 to 0.3.0 (#97)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.2.4 to 0.3.0 (#96)
* :pushpin: Automatic update of dependency thoth-common from 0.16.0 to 0.16.1 (#95)

## Release 0.3.2 (2020-11-26T13:22:35)
### Features
* :lock: Relock Pipfile.lock with package updates (#134)
* Use neutral conclusion if dependencies are not found (#129)
### Automatic Updates
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#132)
* :pushpin: Automatic update of dependency pytest from 6.1.1 to 6.1.2 (#131)
* :pushpin: Automatic update of dependency thoth-common from 0.20.2 to 0.20.4 (#130)
* :pushpin: Automatic update of dependency aiohttp from 3.6.2 to 3.7.2 (#126)
* :pushpin: Automatic update of dependency octomachinery from 0.3.2 to 0.3.4 (#127)
* :pushpin: Automatic update of dependency thoth-common from 0.20.0 to 0.20.2 (#128)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.1 (#123)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.1 (#122)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.3.4 to 0.3.5 (#121)
* :pushpin: Automatic update of dependency pytest from 6.0.2 to 6.1.1 (#120)
* :pushpin: Automatic update of dependency thoth-report-processing from 0.3.4 to 0.3.5 (#119)
* :pushpin: Automatic update of dependency octomachinery from 0.3.0 to 0.3.2 (#118)

## Release 0.3.3 (2021-03-26T02:49:58)
### Features
* Fix the list of maintainers
* update the list of maintainers
* prow config for pre-commit checks
* :arrow_up: Automatic update of dependencies by Kebechet (#147)
* :arrow_up: Automatic update of dependencies by Kebechet (#144)
* :arrow_up: update CI/CD configuration (#145)
* :arrow_up: Automatic update of dependencies by kebechet. (#141)
* :arrow_up: Automatic update of dependencies by kebechet. (#138)
* port to python 38 (#133)

## Release 0.3.4 (2021-03-29T02:25:37)
### Features
* :fire: Reduce the cpu usage for the tasks
* :fire: HOTFIX: Use the explicit pyjwt 1.7.1 for the github app (#153)
