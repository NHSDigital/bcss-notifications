## Oracle thick client mode

The BCSS Oracle database we connect to for processing batches and updating message statuses is configured with network encryption.
This means that the Python oracledb package thin client mode cannot be used to make the various database calls.

We can use thick client mode to connect and execute calls, but this requires some supporting libraries to work with AWS Lambdas.

We publish an Oracle Client lambda layer via a [manual Github workflow](../.github/workflows/deploy-oracleclient-lambda-layer.yml) which contains the Oracle Client libraries downloaded from Oracle's website. Currently the version we use is Version 21.18.0.0.0 (Basic Lite) of the Oracle Client libraries.

The lambda layer is used by both the batch notification processor lambda and the message status handler lambda as they both require database connectivity.

The layer is present and working on the AWS Texas non production environment.


### New environment setup

When provisioning a new environment. The workflow to enable Oracle thick client mode would be:

1. Configure AWS secretsmanager with appropriate secrets for database connectivity.
2. Run the [Deploy Oracle Client lambda layer](../.github/workflows/deploy-oracleclient-lambda-layer.yml) github workflow to create the layer.
3. [Amend the appropriate terraform variables](../terraform/config/development.tfvars) which contain the ARN of the newly created layer and the secretsmanager ARN.
4. Run terraform plan and terraform apply.
5. Deploy other lambda layers (containing the Python dependencies)
6. Deploy the lambda code.
