###!/usr/bin/env bash

set -e

read -p "Enter your UVA computing ID: " uid
read -p "Enter your laptop core count: " cpu
read -p "Enter your laptop memory in GB: " mem
read -p "Enter your laptop HD size in GB: " hds

curl -X POST -H "Content-Type: application/json" -d '{"uid":"'$uid'","cpu":"'$cpu'","mem":"'$mem'","hds":"'$hds'"}' https://8jzxtr9qg5.execute-api.us-east-1.amazonaws.com/api/laptops

echo "Thank you for submitting!"
