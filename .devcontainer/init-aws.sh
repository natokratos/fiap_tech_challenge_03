#!/bin/bash

awslocal s3 mb s3://raw
#awslocal dynamodb create-table \
#    --table-name raw \
#    --key-schema AttributeName=id,KeyType=HASH \
#    --attribute-definitions AttributeName=id,AttributeType=S \
#    --billing-mode PAY_PER_REQUEST
    #--region ap-south-1