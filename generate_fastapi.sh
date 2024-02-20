docker run --rm \
  -v ${PWD}:/local openapitools/openapi-generator-cli generate \
  -i /local/openai_openapi.yaml \
  --skip-validate-spec \
  -g python-fastapi \
  -o /local/src