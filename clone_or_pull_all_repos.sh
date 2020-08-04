#!/bin/bash

# script that makes a local clone of all relevant Fabric8 repositories
# the content of repositories are to be used to generate dashboard

REPO_URL_PREFIX="https://github.com/fabric8-analytics/"

REPOSITORIES="
fabric8-analytics-common
fabric8-analytics-data-model
fabric8-analytics-jobs
fabric8-analytics-license-analysis
fabric8-analytics-recommender
fabric8-analytics-server
fabric8-analytics-stack-analysis
fabric8-analytics-tagger
fabric8-analytics-worker
fabric8-analytics-nvd-toolkit
fabric8-analytics-auth
fabric8-gemini-server
fabric8-analytics-api-gateway
fabric8-analytics-version-comparator
fabric8-analytics-ingestion
fabric8-analytics-npm-insights
fabric8-analytics-jenkins-plugin
fabric8-analytics-notification-scheduler
fabric8-analytics-utils
fabric8-analytics-release-monitor
fabric8-analytics-github-refresh-cronjob
fabric8-analytics-github-events-monitor
fabric8-analytics-rudra
fabric8-analytics-scaler
f8a-server-backbone
f8a-hpf-insights
f8a-golang-insights
f8a-pypi-insights
f8a-stacks-report
f8a-data-ingestion-service
f8a-emr-deployment
cvejob
victimsdb-lib
fabric8-analytics.github.io"

pushd repositories

for repository in $REPOSITORIES
do
    echo $repository
    if [ -d $repository ]
    then
        echo "Pulling changes into $repository"
        pushd $repository
        git pull
        popd
    else
        repo_url="${REPO_URL_PREFIX}${repository}.git"
        echo "Cloning from $repo_url"
        git clone $repo_url
    fi
    echo $repository
done

popd

export F8A_API_URL_STAGE=http://bayesian-api-bayesian-preview.b6ff.rh-idev.openshiftapps.com
export F8A_API_URL_PROD=https://recommender.api.openshift.io

export F8A_JOB_API_URL_STAGE=http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com
export F8A_JOB_API_URL_PROD=http://bayesian-jobs-bayesian-production.09b5.dsaas.openshiftapps.com

export RECOMMENDER_API_TOKEN_STAGE=""
export RECOMMENDER_API_TOKEN_PROD=""

export JOB_API_TOKEN_STAGE=""
export JOB_API_TOKEN_PROD=""

export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export S3_REGION_NAME="us-east-1"

