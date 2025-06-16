#!/bin/bash

lambda_name=$1

build_dir=build/${lambda_name}

rm -rf ${lambda_name}.zip
mkdir -p ${build_dir}
cp ../../../${lambda_name}/*.py ${build_dir}
cp ../../../shared/*.py ${build_dir}
cd ${build_dir}
zip -r ../../${lambda_name}.zip *.py
cd ../..
rm -rf build
